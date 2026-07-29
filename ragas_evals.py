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
from ragas.metrics import faithfulness
from ragas.llms import LangchainLLMWrapper
from langchain_anthropic import ChatAnthropic
from datasets import Dataset

from rag_service import answer_question   # same code path as production
import os
from dotenv import load_dotenv

load_dotenv()
judge = LangchainLLMWrapper(
    ChatAnthropic(model="claude-sonnet-4-5",
                  api_key=os.getenv("CLAUDE_API_KEY"))
)

questions = [
    {"question":    "How do I create a wall in Revit?", "category": "walls"},
    {"question": "What is a floor plan view?",  "category": "floors"}
]

rows = {"user_input": [], "response": [], "retrieved_contexts": []}
refusal_count = 0

for q in questions:
    # your pipeline's real answer
    answer, sources, chunks = answer_question(q["question"], q["category"])
    if answer == "I don't know":
        refusal_count += 1
        continue
    rows["user_input"].append(q["question"])
    rows["response"].append(answer)
    rows["retrieved_contexts"].append([c["text"] for c in chunks])

refusal_rate = refusal_count / len(questions)

if rows["user_input"]:
    data = Dataset.from_dict(rows)
    result = evaluate(data, metrics=[faithfulness], llm=judge)
    df = result.to_pandas()
    print(df[["user_input", "response", "faithfulness"]])
    print(
        f"\nfaithfulness (answered only, n={len(rows['user_input'])}): {df['faithfulness'].mean():.4f}")
else:
    print("faithfulness: n/a (no answered questions)")

print(f"refusal_rate: {refusal_rate:.4f} ({refusal_count}/{len(questions)})")
