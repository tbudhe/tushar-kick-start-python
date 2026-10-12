
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import create_agent
load_dotenv()

TICKERS = {"Yieldnext": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}


@tool(description="Look up the ticker symbol for a company name.")
def get_ticker(company_name: str):
    return TICKERS.get(company_name)


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES[ticker]

# cheap model, fine for this chain
model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))
agent = create_agent(model, [get_ticker, get_price])
result = agent.invoke({"messages": [("user", "Price of Yieldnext?")]})
for m in result["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")