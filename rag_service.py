from retriever import retrieve
from prompting.revit_context_qa import ask_revit_question


def answer_question(question, category=None):
    """The one true RAG pipeline. Used by BOTH app.py and evals.py,
    so evals always test the exact code path production runs."""
    chunks = retrieve(question, category)

    if not chunks:
        # No relevant context -> don't call Claude at all
        return "I don't know", []

    context = "\n".join(c["text"] for c in chunks)
    answer = ask_revit_question([
        {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
    ])
    sources = [c["id"] for c in chunks]

    return answer, sources
