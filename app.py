from fastapi import FastAPI
from pydantic import BaseModel
from rag_service import answer_question

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
    answer, sources = answer_question(req.question)
    return AskResponse(answer=answer, sources=sources)