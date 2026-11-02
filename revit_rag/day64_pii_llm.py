import os
import re
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\b\d{3}[-.]\d{3}[-.]\d{4}\b",
}

def redact(text):
    found = {}
    for label, pattern in PATTERNS.items():
        for i, value in enumerate(re.findall(pattern, text)):
            tag = f"[{label}_{i}]"
            found[tag] = value
            text = text.replace(value, tag)
    return text, found

def restore(text, found):
    for tag, value in found.items():
        text = text.replace(tag, value)
    return text

question = ("I'm Jo, email jo@acme.com, phone 973-555-1234. "
            "Write a one-line reply confirming we'll email the wall guide.")

safe, found = redact(question)
print("SENT TO LLM:", safe)
def ask(text):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=200,
        system="Keep placeholders like [EMAIL_0] exactly as written.",
        messages=[{"role": "user", "content": text}],
    )
    return response.content[0].text

answer = ask(safe)
print("LLM REPLY:  ", answer)
print("TO USER:    ", restore(answer, found))

probe = " What is the user's exact email address? Reply with only the address."
print("PROBE redacted:", ask(safe + probe))
print("PROBE raw:     ", ask(question + probe))