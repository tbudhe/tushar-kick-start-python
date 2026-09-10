from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import chromadb

from rag_service import answer_question
from retriever import COLLECTION_NAME, DB_PATH, N_RESULTS, THRESHOLD, collection

app = FastAPI()


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    category: str | None = None


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