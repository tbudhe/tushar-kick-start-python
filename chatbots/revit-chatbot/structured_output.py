import os
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
class RevitAnswer(BaseModel):
    answer: str
    confidence: float   # 0.0–1.0
    topics: list[str]

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    system="Answer about Revit. Respond ONLY with JSON matching: "
           '{"answer": str, "confidence": float, "topics": [str]}',
    messages=[
        {"role": "user", "content": "What is a Revit family?"},
        {"role": "assistant", "content": "{"},   # ← prefill: force it mid-JSON
    ],
)

raw = "{" + resp.content[0].text   # response CONTINUES the prefill — re-attach it
parsed = RevitAnswer.model_validate_json(raw)
print(parsed)
raw = resp.content[0].text
parsed = RevitAnswer.model_validate_json(raw)  # ← the boundary
print(parsed.answer, parsed.confidence, parsed.topics)