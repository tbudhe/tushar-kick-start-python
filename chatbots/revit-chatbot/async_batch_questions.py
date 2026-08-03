import asyncio
import os
from anthropic import AsyncAnthropic   # async client, note the name
from dotenv import load_dotenv

load_dotenv()
client = AsyncAnthropic(api_key=os.getenv("CLAUDE_API_KEY"))


async def ask(question: str) -> tuple[str, str]:  # async def = async function
    msg = await client.messages.create(        # await = same as JS await
        model="claude-sonnet-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": question}],
    )
    return msg.content[0].text, msg.stop_reason



async def main():
    questions = ["What is a Revit wall?", "What is a floor?", "What is a roof?"]
    results = await asyncio.gather(*(ask(q) for q in questions))  # Promise.all
    for q, (a, stop_reason) in zip(questions, results):
        print(f"Q: {q}\nstop_reason: {stop_reason}, len: {len(a)}\nA: {a[:60]}...\n")


asyncio.run(main())    # the one thing JS doesn't have: you start the event loop yourself
