"""Day 74 step 3 - RAG pipeline vs the LangSmith dataset, judged by Claude."""
import os
import anthropic
from dotenv import load_dotenv
from langsmith import evaluate
from revit_rag.rag_service import answer_question
load_dotenv()
claude = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
DATASET = "revit-rag-golden"


def target(inputs: dict) -> dict:
    """The app under test: question in -> answer + the chunks it used out."""
    response = answer_question(inputs["question"])
    return {
        "answer": response.answer,
        "chunks": "\n".join(s.text for s in response.sources),
        "refused": response.refused,
    }


def faithful(inputs: dict, outputs: dict) -> dict:
    """LLM-as-judge (same rubric as day62): every claim backed by the chunks?"""
    if outputs["refused"]:
        return {"key": "faithful", "score": None, "comment": "refused - nothing to judge"}
    prompt = (f"Context:\n{outputs['chunks']}\n\nQuestion: {inputs['question']}\n"
              f"Answer: {outputs['answer']}\n\nIs EVERY claim in the Answer supported "
              "by the Context? Reply with exactly one word: YES or NO.")
    reply = claude.messages.create(model="claude-opus-4-8", max_tokens=5,
                                   messages=[{"role": "user", "content": prompt}])
    verdict = reply.content[0].text.strip()
    return {"key": "faithful", "score": 1 if verdict == "YES" else 0, "comment": verdict}


results = evaluate(target, data=DATASET, evaluators=[faithful],
                   experiment_prefix="revit-rag-haiku")
print("experiment:", results.experiment_name)
# --- Step 4: EVAL GATE - fail the build if faithfulness drops ---
import sys

THRESHOLD = 0.75
scores = []
for row in results:                                   # one row per dataset example
    question = row["example"].inputs["question"]
    result = row["evaluation_results"]["results"][0]  # our single 'faithful' evaluator
    print(f"{question:34} -> {result.score}  ({result.comment})")
    if result.score is not None:                      # refused rows have nothing to judge
        scores.append(result.score)

faithfulness = sum(scores) / len(scores) if scores else 0.0
print(f"\nfaithfulness: {faithfulness:.2f}   (threshold {THRESHOLD})")
if faithfulness < THRESHOLD:
    print("EVAL GATE: FAIL")
    sys.exit(1)                                       # non-zero = CI marks the job red
print("EVAL GATE: PASS")