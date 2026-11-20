"""Day 75 - prove the eval gate FAILS on a bad answer (exit code 1)."""
import os
import sys
import anthropic
from dotenv import load_dotenv
from langsmith import evaluate
from revit_rag.rag_service import answer_question

load_dotenv()
claude = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
DATASET = "revit-rag-golden"
THRESHOLD = 0.75
FAKE = "In Revit you must buy a Fusion licence and paint every wall blue first."


def target(inputs: dict) -> dict:
    """Simulates a bad prompt/model change: real chunks, made-up answer."""
    response = answer_question(inputs["question"])
    return {"answer": FAKE,
            "chunks": "\n".join(s.text for s in response.sources),
            "refused": response.refused}


def faithful(inputs: dict, outputs: dict) -> dict:
    """Same judge as day74: is every claim backed by the chunks?"""
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
                   experiment_prefix="revit-rag-broken")
scores = []
for row in results:
    result = row["evaluation_results"]["results"][0]
    print(f"{row['example'].inputs['question']:34} -> {result.score}  ({result.comment})")
    if result.score is not None:
        scores.append(result.score)

faithfulness = sum(scores) / len(scores) if scores else 0.0
print(f"\nfaithfulness: {faithfulness:.2f}   (threshold {THRESHOLD})")
if faithfulness < THRESHOLD:
    print("EVAL GATE: FAIL")
    sys.exit(1)
print("EVAL GATE: PASS")