from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AskRequest(BaseModel):
    question: str          # required, must be a string

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
   
@app.get("/heartbeat")
def heartbeat() -> dict[str, str]:
    return {"status": "OK"}

@app.post("/ask")
def ask(req: AskRequest) -> AskResponse:
    # req.question is guaranteed to exist and be a str here
    return AskResponse(answer="stub", sources=[])