"""Day 76 step 3 - time each step of one RAG request (plain-code stopwatch)."""
from dotenv import load_dotenv
load_dotenv()
import time
from langsmith import traceable
from revit_rag import rag_service


def stopwatch(name, fn):
    """Wrap fn: start the clock, run the REAL function, stop the clock."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)          # the real work happens HERE
        print(f"{name:10}: {time.time() - start:.2f}s")
        return result
    return wrapper


# swap the names inside rag_service (attaching only - nothing runs yet)
rag_service.retrieve = stopwatch("retrieve", rag_service.retrieve)
rag_service.ask_revit_question = stopwatch("ask_claude", rag_service.ask_revit_question)
traced_answer = traceable(name="answer_question")(rag_service.answer_question)

start = time.time()
response = traced_answer("How do I place a door?")   # retrieve + ask_claude run inside this
print(f"{'total':10}: {time.time() - start:.2f}s")
print("answer:", response.answer[:60])