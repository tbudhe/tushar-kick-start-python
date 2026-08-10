import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
load_dotenv()


class Source(BaseModel):
    doc_id: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=1.0)


class RevitAnswer(BaseModel):
    answer: str = Field(min_length=1)            # no empty answers
    confidence: float = Field(ge=0.0, le=1.0)    # ge/le = >= and <=
    topics: list[str] = Field(min_length=1)      # at least one topic
    caveat: Optional[str] = None   # may be absent; defaults to None
    sources: list[Source] = Field(min_length=1)   # list of nested objects


# valid = '''{"answer": "x", "confidence": 0.9, "topics": ["Revit"],
#   "sources": [{"doc_id": "d1", "score": 0.8}, {"doc_id": "d2", "score": 0.7}]}'''
# print(RevitAnswer.model_validate_json(valid))

bad = '''{"answer": "x", "confidence": 0.9, "topics": ["Revit"],
  "sources": [{"doc_id": "d1", "score": 0.8}, {"doc_id": "d2", "score": 1.5}]}'''
try:
    RevitAnswer.model_validate_json(bad)
except Exception as e:
    print(f"Validation error: {e}")

