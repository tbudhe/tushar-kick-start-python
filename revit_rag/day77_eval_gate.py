"""Day 77 step 2 - eval gate for CI: reasons on every NO, 3 repetitions per question."""
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


def target(inputs: dict) -> dict:
    response = answer_question(inputs["question"])
    return {"answer": response.answer,
            "chunks": "\n".join(s.text for s in response.sources),
            "refused": response.refused}


def faithful(inputs: dict, outputs: dict) -> dict:
    if outputs["refused"]:
        return {"key": "faithful", "score": None, "comment": "refused - nothing to judge"}
    prompt = (f"Context:\n{outputs['chunks']}\n\nQuestion: {inputs['question']}\n"
              f"Answer: {outputs['answer']}\n\nIs EVERY claim in the Answer supported "
              "by the Context? Reply YES, or reply NO followed by the one claim "
              "that is not supported, quoted from the Answer.")          # Day 77: ask for the reason
    reply = claude.messages.create(model="claude-opus-4-8", max_tokens=100,
                                   messages=[{"role": "user", "content": prompt}])
    verdict = reply.content[0].text.strip()
    score = 1 if verdict.startswith("YES") else 0                       # Day 77: reason follows NO
    return {"key": "faithful", "score": score, "comment": verdict}


results = evaluate(target, data=DATASET, evaluators=[faithful],
                   experiment_prefix="revit-rag-ci", num_repetitions=3)  # Day 77: 3 reps
print("experiment:", results.experiment_name)

scores = []
for row in results:
    question = row["example"].inputs["question"]
    result = row["evaluation_results"]["results"][0]
    print(f"{question:34} -> {result.score}  ({result.comment[:80]})")
    if result.score is not None:
        scores.append(result.score)

faithfulness = sum(scores) / len(scores) if scores else 0.0
print(f"\nfaithfulness: {faithfulness:.2f} over {len(scores)} judged rows (threshold {THRESHOLD})")
if faithfulness < THRESHOLD:
    print("EVAL GATE: FAIL")
    sys.exit(1)
print("EVAL GATE: PASS")