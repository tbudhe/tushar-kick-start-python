
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


@tool(description="Look up the ticker symbol for a company name.")
def get_ticker(company_name: str):
    return TICKERS.get(company_name)


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    time.sleep(2)                 # simulate a slow downstream call
    return PRICES.get(ticker)


SYSTEM_PROMPT = (
    "You are a stock price assistant with two tools: get_ticker (company name -> ticker) "
    "and get_price (ticker -> price). "
    "If the user gives a company name, call get_ticker first, then call get_price with the "
    "result. If the user already gives a ticker symbol, call get_price directly. "
    "Never guess a ticker or price yourself - always use the tools. "
    "If get_ticker returns nothing, tell the user the company isn't recognized instead of "
    "calling get_price. "
    "Respond with the final price formatted as a dollar amount, e.g. '$189.50'."
)

model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))
agent_no_check_pointer = create_agent(
    model, [get_ticker, get_price], system_prompt=SYSTEM_PROMPT)


print("=== PART A: updates ===")

for chunk in agent_no_check_pointer.stream(
    {"messages": [HumanMessage("What is the price of Yieldnext?")]},
    stream_mode="updates",
):
    for node, payload in chunk.items():        # node -> "model" or "tools"
        msg = payload["messages"][-1]          # <-- msg is created HERE
        if getattr(msg, "tool_calls", None):
            print(f"[{node}] tool_calls: {[tc['name'] for tc in msg.tool_calls]}")
        elif node == "tools":
            print(f"[{node}] result: {msg.content}")
        else:
            print(f"[{node}] text: {msg.content}")

print("\n=== PART B: values ===")

for step, chunk in enumerate(agent_no_check_pointer.stream(
    {"messages": [HumanMessage("What is the price of Yieldnext?")]},
    stream_mode="values",
), start=1):
    msgs = chunk["messages"]
    last = msgs[-1]
    print(f"step {step}: {len(msgs)} messages -> {type(last).__name__}")

print("\n=== PART C: messages (tokens) ===")

last_ts = time.time()

for token, metadata in agent_no_check_pointer.stream(
    {"messages": [HumanMessage("What is the price of Yieldnext?")]},
    stream_mode="messages",
):
    now = time.time()
    gap = now - last_ts
    last_ts = now

    if gap > 0.4:
        print(f"\n  <-- silent gap {gap:.1f}s -->")

    c = token.content
    if isinstance(c, str):
        text = c
    elif isinstance(c, list):
        text = "".join(b.get("text", "") for b in c if isinstance(b, dict))
    else:
        text = ""

    if text:
        print(text, end="|", flush=True)
    print(f"\n[{metadata.get('langgraph_node')}] raw={token.content!r}")
