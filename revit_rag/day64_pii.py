import re

PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\b\d{3}[-.]\d{3}[-.]\d{4}\b",
    "CARD": r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",
}

def redact(text):
    found = {}                                  # placeholder -> real value
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

safe, found = redact("Card 4111-1111-1111-1111, mail jo@acme.com, call 973-555-1234")
print(safe)
print(found)