
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

MAX_ITERATIONS = 10


def call_model(messages):
    response = client.messages.create(
        model="claude-sonnet-5", max_tokens=500,
        tools=TOOLS, messages=messages)
    return response


def handle_tools(response, messages):
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
    messages.append({"role": "user", "content": results})
    return messages


def give_up(messages):
    # last message is always the user-role tool_result block handle_tools just
    # appended — add a text block to it instead of a new message, so the
    # transcript stays alternating (no back-to-back user turns)
    messages[-1]["content"].append({
        "type": "text",
        "text": ("You've used all available tool-call attempts for this turn. "
                 "Answer now with whatever you were able to find, and tell the "
                 "user plainly that you weren't able to finish."),
    })
    # no tools kwarg — model can't request another call, only produce text
    return client.messages.create(
        model="claude-sonnet-5", max_tokens=500, messages=messages)


def run_agent(user_message):
    messages = [{"role": "user", "content": user_message}]
    for iteration in range(MAX_ITERATIONS):        # not while True
        response = call_model(messages)
        if response.stop_reason != "tool_use":
            # model says it's done
            return response
        messages.append({"role": "assistant", "content": response.content})
        messages = handle_tools(response, messages)
    # ceiling hit — loop exhausted without finishing
    # defined behavior, not a crash
    return give_up(messages)


final = run_agent(
    "What's Apple's stock price, and confirm the company name first?")
print(final.content[-1].text)
