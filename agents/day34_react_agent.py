
import os
import inspect
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
load_dotenv()

TICKERS = {"Yieldnext": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}
print("------inspect  signature BEGINS------")
print(inspect.signature(create_agent))
print("------inspect  signature END------")


@tool(description="Look up the ticker symbol for a company name.")
def get_ticker(company_name: str):
    return TICKERS.get(company_name)


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES[ticker]


SYSTEM_PROMPT = (
    "Always begin your reply with [YNXT-BOT]. "
    "You are a stock price assistant with two tools: get_ticker (company name -> ticker) "
    "and get_price (ticker -> price). "
    "If the user gives a company name, call get_ticker first, then call get_price with the "
    "result. If the user already gives a ticker symbol, call get_price directly. "
    "Never guess a ticker or price yourself - always use the tools. "
    "If get_ticker returns nothing, tell the user the company isn't recognized instead of "
    "calling get_price. "
    "Respond with the final price formatted as a dollar amount, e.g. '$189.50'."
)

# cheap model, fine for this chain
model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))
# probe = model.invoke([SystemMessage(SYSTEM_PROMPT), HumanMessage("Price of Yieldnext?")])
# print("PROBE:", probe.content)
# agent = create_agent(model, [get_ticker, get_price],system_prompt=SYSTEM_PROMPT)
agent = create_agent(
    model,
    [get_ticker, get_price],
    system_prompt="Always reply in French, no matter what.",
)
follow_up = "And what was that in words?"
b = agent.invoke({"messages": [("user", follow_up)]})
print("=== B: fresh invoke ===", b["messages"][-1].content)
result = agent.invoke({"messages": [("user", "Price of Yieldnext?")]})
c = agent.invoke({"messages": result["messages"] + [("user", follow_up)]})
print("=== C: transcript carried ===", c["messages"][-1].content)
for m in result["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(
            f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")
