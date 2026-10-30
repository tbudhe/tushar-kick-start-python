"""Day 62 — faithfulness eval: LLM-as-judge over the real RAG pipeline."""
from revit_rag.rag_service import answer_question

question = "How do I add a door to a wall?"
response = answer_question(question)

print("ANSWER:", response.answer)
print("SOURCES:", [s.id for s in response.sources])
print("REFUSED:", response.refused)

"""Day 62 — faithfulness eval: LLM-as-judge over the real RAG pipeline."""
import os
import anthropic
from dotenv import load_dotenv
from revit_rag.rag_service import answer_question

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])


def judge_faithful(question, chunks, answer):
    prompt = f"""Context:\n{chunks}\n\nQuestion: {question}\nAnswer: {answer}

Is EVERY claim in the Answer supported by the Context?
Reply with exactly one word: YES or NO."""
    reply = client.messages.create(
        model="claude-opus-4-8", max_tokens=5,
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.content[0].text.strip()


question = "How do I add a door to a wall?"
response = answer_question(question)
chunks = "\n".join(s.text for s in response.sources)

print("ANSWER:", response.answer[:80], "...")
print("JUDGE:", judge_faithful(question, chunks, response.answer))