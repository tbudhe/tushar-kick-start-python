
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
load_dotenv()

TICKERS = {"YUNextGenAI": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}


@tool(description="Look up the ticker symbol for a company name.")
def get_ticker(company_name: str):
    return TICKERS[company_name]


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES[ticker]


TOOLS_BY_NAME = {"get_ticker": get_ticker, "get_price": get_price}

# cheap model, fine for this chain
model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools([get_ticker, get_price])  # staple once

MAX_ITERATIONS = 5


def invoke(messages):
    for round_num in range(MAX_ITERATIONS):        # not while True
        print(f"=== ROUND {round_num} ===")
        response = model_with_tools.invoke(messages)   # an AIMessage
        messages.append(response)
        if not response.tool_calls:
            return response
        for tc in response.tool_calls:                 # already parsed: {name, args, id}
            print("model requested:", tc["name"] + str(tc["args"]))
            tool_msg = TOOLS_BY_NAME[tc["name"]].invoke(tc)  # returns a ToolMessage, id pre-matched
            print("tool result:", tool_msg.content)
            messages.append(tool_msg)
    return response


messages = [HumanMessage("What's a stock price for YUNextGenAI?")]
final = invoke(messages)
print(final)
