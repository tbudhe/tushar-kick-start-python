
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
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
    "description":  "Get the company name for a given stock ticker symbol. Use when the user asks what company a ticker belongs to.",
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


class StockPriceInput(BaseModel):
    ticker: str


def get_stock_price_strict(ticker):
    if ticker != "AAPL":
        raise ValueError(f"unknown ticker '{ticker}'")
    return PRICES[ticker]


def get_company_name(ticker):
    if ticker not in NAMES:
        raise ValueError(f"unknown ticker '{ticker}' — known: {list(NAMES)}")
    return NAMES[ticker]


TOOL_FUNCTIONS = {"get_stock_price": get_stock_price_strict,
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
                try:
                    args = StockPriceInput.model_validate(block.input)
                    result = TOOL_FUNCTIONS[block.name](**args.model_dump())
                    is_error = False
                except ValidationError as e:
                    result = f"Invalid arguments: {e}"
                    is_error = True
                except Exception as e:
                    result = f"Tool failed: {e}"
                    is_error = True
                print("tool call:", block.name, block.input)   # evidence
                results.append({"type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result),
                                "is_error": is_error})
        # transcript grows
        messages.append({"role": "user", "content": results})
        print("messages:", messages)


final = run_conversation(
    "What's the current price of Google stock? Use the company lookup first to confirm the ticker.")
print(final.content[-1].text)
