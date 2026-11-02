from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

SYSTEM_PROMPT = (
    "You are an Autodesk Revit documentation assistant. "
    "Answer ONLY using the context provided in the user's message. "
    "If the context does not contain the answer, reply exactly: I don't know. "
    "Keep answers to 2-3 sentences."
)


def ask_revit_question(messages):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return response.content[0].text
