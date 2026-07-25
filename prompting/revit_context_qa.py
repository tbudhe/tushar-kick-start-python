from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

system = (
    "You are an Autodesk Revit documentation assistant. "
    "Answer ONLY using the context provided in the user's message. "
    "If the context does not contain the answer, reply exactly: I don't know. "
    "Keep answers to 2-3 sentences."
)


def ask_revit_question(messages):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=system,
        messages=messages
    )
    return response.content[0].text
