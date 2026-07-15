import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

question = "A store had 23 apples. They sold 8, then got a shipment of 15 more. How many apples now?"

# Without chain-of-thought - forces an instant answer
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=50,
    messages=[{"role": "user", "content": f"{question} Answer with just the number."}]
)
print("Direct:", response.content[0].text)

# With chain-of-thought - lets it reason first
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=300,
    messages=[{"role": "user", "content": f"{question} Think step by step before giving the final answer."}]
)
print("Chain-of-thought:", response.content[0].text)
