import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
load_dotenv()


class RevitAnswer(BaseModel):
    answer: str = Field(min_length=1)            # no empty answers
    confidence: float = Field(ge=0.0, le=1.0)    # ge/le = >= and <=
    topics: list[str] = Field(min_length=1)      # at least one topic
    caveat: Optional[str] = None   # may be absent; defaults to None


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

# no_topics = '{"answer": "x", "confidence": 0.9, "topics": ["a"]}'
# RevitAnswer.model_validate_json(no_topics)
