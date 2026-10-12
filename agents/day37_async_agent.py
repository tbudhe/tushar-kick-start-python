import asyncio
import os
import time
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

load_dotenv()

TICKERS = {"Yieldnext": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}
T0 = time.time()


def stamp(msg: str):
    print(f"    [t+{time.time() - T0:5.2f}s] {msg}")


@tool(description="Look up the ticker symbol for a company name.")
async def get_ticker(company_name: str):
    stamp(f"get_ticker({company_name!r}) START")
    await asyncio.sleep(2)
    stamp(f"get_ticker({company_name!r}) END")
    return TICKERS.get(company_name)


@tool(description="Get the current stock price for a ticker symbol.")
async def get_price(ticker: str):
    stamp(f"get_price({ticker!r}) START")
    await asyncio.sleep(2)
    stamp(f"get_price({ticker!r}) END")
    return PRICES.get(ticker)


SYSTEM_PROMPT = (
    "You are a stock price assistant with two tools: get_ticker (company name -> ticker) "
    "and get_price (ticker -> price). "
    "If the user gives a company name, call get_ticker first, then call get_price with the "
    "result. If the user already gives a ticker symbol, call get_price directly. "
    "Never guess a ticker or price yourself - always use the tools. "
    "Respond with each price formatted as a dollar amount, e.g. '$189.50'."
)

model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))

agent = create_agent(model, [get_ticker, get_price],
                     system_prompt=SYSTEM_PROMPT)


async def part_a():
    global T0
    print("=== PART A: two INDEPENDENT tool calls, one round ===")
    T0 = time.time()
    result = await agent.ainvoke(
        {"messages": [HumanMessage("What are the prices of YNXT and AAPL?")]}
    )
    print(result["messages"][-1].content)
    print(f"wall clock: {time.time() - T0:.1f}s")


async def part_b():
    global T0
    print("\n=== PART B: DEPENDENT chain (name -> ticker -> price) ===")
    T0 = time.time()
    result = await agent.ainvoke(
        {"messages": [HumanMessage("What is the price of Yieldnext?")]}
    )
    print(result["messages"][-1].content)
    print(f"wall clock: {time.time() - T0:.1f}s")

async def part_c():
    global T0

    def q(text: str):
        return {"messages": [HumanMessage(text)]}

    print("\n=== PART C-1: two agent runs, SERIAL ===")
    T0 = time.time()
    await agent.ainvoke(q("What is the price of Yieldnext?"))
    await agent.ainvoke(q("What is the price of Apple?"))
    print(f"wall clock: {time.time() - T0:.1f}s")

    print("\n=== PART C-2: two agent runs, CONCURRENT ===")
    T0 = time.time()
    r1, r2 = await asyncio.gather(
        agent.ainvoke(q("What is the price of Yieldnext?")),
        agent.ainvoke(q("What is the price of Apple?")),
    )
    print("run1:", r1["messages"][-1].content)
    print("run2:", r2["messages"][-1].content)
    print(f"wall clock: {time.time() - T0:.1f}s")

async def main():
    await part_a()
    await part_b()
    await part_c()

asyncio.run(main())
