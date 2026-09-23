import os

import anthropic
from dotenv import load_dotenv
load_dotenv()                                     # read .env into os.environ
client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
# the only labels your graph has nodes for
ROUTES = {"price", "docs", "greet"}

SYSTEM = ("Classify the user's MAIN request. Reply with exactly one word: "
          "price, docs, or greet. If there is a greeting AND a real question, "
          "choose the real question.")


def llm_route(question):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=5,                  # one word, so keep it tiny
        system=SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    label = response.content[0].text.strip().lower()   # " Price." -> "price."
    label = label.strip(".")                            # "price." -> "price"
    # safety net: unknown label -> docs
    return label if label in ROUTES else "docs"


if __name__ == "__main__":
    for q in ["hi there", "How much does Fusion cost?", "hi, how much does Fusion cost?"]:
        print(q, "->", llm_route(q))
