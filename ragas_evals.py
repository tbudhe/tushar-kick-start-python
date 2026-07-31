import sys
import types

# ragas (as of 0.4.3) unconditionally imports langchain_community's VertexAI
# chat model at import time, just for an isinstance() check we never hit here
# (we only use ChatAnthropic). That submodule was removed from the installed
# langchain-community release, so ragas fails to import at all. Stub it out
# before importing ragas rather than downgrading langchain-community, which
# would break the rest of this repo's (newer) langchain stack.
if "langchain_community.chat_models.vertexai" not in sys.modules:
    _vertexai_stub = types.ModuleType(
        "langchain_community.chat_models.vertexai")

    class ChatVertexAI:  # placeholder; never instantiated
        pass

    _vertexai_stub.ChatVertexAI = ChatVertexAI
    sys.modules["langchain_community.chat_models.vertexai"] = _vertexai_stub

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from datasets import Dataset

from rag_service import answer_question   # same code path as production
import os
from dotenv import load_dotenv

load_dotenv()
judge_llm = LangchainLLMWrapper(
    ChatAnthropic(model="claude-sonnet-4-5",
                  api_key=os.getenv("CLAUDE_API_KEY"))
)

judge_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)
EVAL_QUESTIONS = [
    {"question": "How do I create a wall in Revit?", "category": "walls",
        "reference": "Use the Wall tool on the Architecture tab, pick a wall type, then draw the wall in the view."},
    {"question": "What is a floor plan view?", "category": "floors",
        "reference": "A floor plan view is a horizontal view of a building level in Revit, showing walls, doors, and rooms from above."},
]

eval_rows = {"user_input": [], "response": [],
             "retrieved_contexts": [], "reference": []}
refusal_count = 0

for case in EVAL_QUESTIONS:
    # your pipeline's real answer
    answer, sources, chunks = answer_question(case["question"], case["category"])
    if answer == "I don't know":
        refusal_count += 1
        continue
    eval_rows["user_input"].append(case["question"])
    eval_rows["response"].append(answer)
    eval_rows["retrieved_contexts"].append([c["text"] for c in chunks])
    eval_rows["reference"].append(case["reference"])

refusal_rate = refusal_count / len(EVAL_QUESTIONS)

if eval_rows["user_input"]:
    data = Dataset.from_dict(eval_rows)
    result = evaluate(data, metrics=[
                      faithfulness, answer_relevancy, context_precision], llm=judge_llm, embeddings=judge_embeddings)
    results_df = result.to_pandas()
    print(results_df[["user_input", "response", "faithfulness",
          "answer_relevancy", "context_precision"]])
    print(
        f"\nfaithfulness (answered only, n={len(eval_rows['user_input'])}): {results_df['faithfulness'].mean():.4f}")
else:
    print("faithfulness: n/a (no answered questions)")

print(f"refusal_rate: {refusal_rate:.4f} ({refusal_count}/{len(EVAL_QUESTIONS)})")
