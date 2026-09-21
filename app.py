import time

from fastapi import FastAPI, HTTPException, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import chromadb

from image_split import MAX_DEPTH, UnreadableImage, split_image
from rag_service import answer_question
from retriever import COLLECTION_NAME, DB_PATH, N_RESULTS, THRESHOLD, collection

app = FastAPI()

# Decoding happens in memory, so the cap is a memory budget, not a disk one.
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@app.middleware("http")
async def log_latency(req: Request, call_next):
    # perf_counter, not time(): a wall-clock jump would corrupt the duration.
    start = time.perf_counter()
    response = await call_next(req)
    latency_ms = (time.perf_counter() - start) * 1000
    print(f"[api] {req.method} {req.url.path} {response.status_code} {latency_ms:.1f}ms")
    return response


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    category: str | None = None


class TileOut(BaseModel):
    # "nw/se" = north-west quadrant, then its south-east quadrant.
    path: str
    x: int
    y: int
    width: int
    height: int
    image: str  # base64-encoded PNG


class SplitResponse(BaseModel):
    format: str
    depth: int
    width: int
    height: int
    tiles: list[TileOut]


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    # Declared by the branch that DECIDED. HTTP callers read this flag —
    # they never string-match the answer text to infer a refusal.
    refused: bool


@app.exception_handler(RequestValidationError)
def bad_request(request: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={
            "code": "BAD_REQUEST",
            "field": ".".join(str(p) for p in first["loc"][1:]),
            "message": first["msg"],
        },
    )


@app.exception_handler(HTTPException)
def http_error(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, dict) else {
        "code": "ERROR", "message": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=detail)


@app.get("/heartbeat")
def heartbeat() -> dict[str, str]:
    return {"status": "OK"}


@app.get("/health")
def health() -> dict:
    # _embedding_function is private and may be None when Chroma resolves the
    # embedder from the collection schema instead of an explicit argument.
    ef = getattr(collection, "_embedding_function", None)
    return {
        "status": "ok",
        "collection": COLLECTION_NAME,
        "chunks": collection.count(),
        "db_path": DB_PATH,
        "embedder": type(ef).__name__ if ef is not None else "chroma-schema-default",
        "chromadb": chromadb.__version__,
        "threshold": THRESHOLD,
        "n_results": N_RESULTS,
    }


@app.post("/ask")
def ask(req: AskRequest) -> AskResponse:
    try:
        resp = answer_question(req.question, req.category)
    except Exception as exc:
        # Stable code for the client; the class name is enough to triage
        # without leaking a stack trace or the prompt.
        raise HTTPException(
            status_code=502,
            detail={"code": "UPSTREAM_ERROR", "message": type(exc).__name__},
        ) from exc
    return AskResponse(
        answer=resp.answer,
        sources=[s.id for s in resp.sources],
        refused=resp.refused,
    )

@app.post("/split")
async def split(
    file: UploadFile,
    depth: int = Query(1, ge=1, le=MAX_DEPTH),
) -> SplitResponse:
    """Quad-tree split one image into 4**depth tiles."""
    data = await file.read()
    if not data:
        raise HTTPException(
            status_code=400,
            detail={"code": "EMPTY_UPLOAD", "message": "file is empty"},
        )
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail={
                "code": "FILE_TOO_LARGE",
                "message": f"limit is {MAX_UPLOAD_BYTES} bytes",
            },
        )
    try:
        tiles, width, height = split_image(data, depth)
    except UnreadableImage as exc:
        # The message is ours, not Pillow's — no library internals on the wire.
        raise HTTPException(
            status_code=400,
            detail={"code": "BAD_IMAGE", "message": str(exc)},
        ) from exc

    return SplitResponse(
        format="png",
        depth=depth,
        width=width,
        height=height,
        tiles=[
            TileOut(
                path=t.path,
                x=t.x,
                y=t.y,
                width=t.width,
                height=t.height,
                image=t.png_b64,
            )
            for t in tiles
        ],
    )
