"""Day 62/63 — faithfulness eval: LLM-as-judge over the real RAG pipeline."""
import os
import anthropic
from dotenv import load_dotenv
from revit_rag.rag_service import answer_question

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])

QUESTIONS = [
    "How do I create a wall in Revit?",
    "How do I add a door to a wall?",
    "How do I place a window?",
    "What is a floor plan view?",
    "How do I export a model to DWG?",
]


def judge_faithful(question, chunks, answer):
    prompt = f"""Context:\n{chunks}\n\nQuestion: {question}\nAnswer: {answer}

Is EVERY claim in the Answer supported by the Context?
Reply with exactly one word: YES or NO."""
    reply = client.messages.create(
        model="claude-opus-4-8", max_tokens=5,
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.content[0].text.strip()


yes, answered, refused = 0, 0, 0
for question in QUESTIONS:
    response = answer_question(question)
    if response.refused:              # no claims to judge -> count separately
        refused += 1
        print(f"{question:34} -> REFUSED")
        continue
    chunks = "\n".join(s.text for s in response.sources)
    verdict = judge_faithful(question, chunks, response.answer)
    answered += 1
    if verdict == "YES":
        yes += 1
    print(f"{question:34} -> {verdict}")

print(f"\nfaithfulness: {yes}/{answered} answered  |  refusal_rate: {refused}/{len(QUESTIONS)}")

# --- Step 2: test the tester — real chunks, invented answer ---
door_q = "How do I add a door to a wall?"
door_chunks = "\n".join(s.text for s in answer_question(door_q).sources)
fake = "Press Ctrl+D to place a door, then set its fire rating to 90 minutes."
print(f"\nFAKE ANSWER -> {judge_faithful(door_q, door_chunks, fake)}   (expected NO)")