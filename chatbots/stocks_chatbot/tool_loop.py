
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

TOOLS = [{
    "name": "get_stock_price",
    "description": "Get the current stock price for a ticker symbol. Use when the user asks about a stock's price.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {"type": "string", "description": "Ticker symbol, e.g. 'AAPL'"},
        },
        "required": ["ticker"],
    },
},
    {
    "name": "get_company_name",
    "description": "Get the current stock ticker symbol. Use when the user asks about a  Company Name.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {"type": "string", "description": "Ticker symbol, e.g. 'AAPL'"},
        },
        "required": ["ticker"],
    }
}]

PRICES = {"AAPL": 189.50, "MSFT": 402.10}
NAMES = {"AAPL": "Apple Inc.", "MSFT": "Microsoft Corp."}


def get_stock_price(ticker):
    return PRICES.get(ticker, "unknown ticker")


def get_company_name(ticker):
    return NAMES.get(ticker, "unknown ticker")


TOOL_FUNCTIONS = {"get_stock_price": get_stock_price,
                  "get_company_name": get_company_name}   # dynamic dispatch


def run_conversation(user_input):
    # transcript starts here
    messages = [{"role": "user", "content": user_input}]
    while True:                                            # THE tool loop
        response = client.messages.create(
            model="claude-sonnet-5", max_tokens=500,
            tools=TOOLS, messages=messages)
        print("stop_reason:", response.stop_reason)        # evidence
        if response.stop_reason != "tool_use":
            return response                                # model answered -> done
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print("tool call:", block.name, block.input)   # evidence
                result = TOOL_FUNCTIONS[block.name](**block.input)
                results.append({"type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result)})
        # transcript grows
        messages.append({"role": "user", "content": results})

run_conversation("What's the current price of Apple stock? Use the company lookup first to confirm the ticker.")