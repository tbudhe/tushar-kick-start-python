from retriever import retrieve
from prompting.revit_context_qa import ask_revit_question
from pydantic import BaseModel


class Source(BaseModel):
    id: str
    text: str
    distance: float


class RagResponse(BaseModel):
    answer: str
    sources: list[Source]
    category: str | None = None


def answer_question(question, category=None):
    """The one true RAG pipeline. Used by BOTH app.py and evals.py,
    so evals always test the exact code path production runs."""
    chunks = retrieve(question, category)

    if not chunks:
        # No relevant context -> don't call Claude at all
        return RagResponse(answer="I don't know based on the available docs.", sources=[], category=category)

    context = "\n".join(c["text"] for c in chunks)
    answer = ask_revit_question([
        {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
    ])
    return RagResponse(
        answer=answer,
        sources=[Source(id=c["id"], text=c["text"],
                        distance=c["distance"]) for c in chunks],
        category=category
    )
