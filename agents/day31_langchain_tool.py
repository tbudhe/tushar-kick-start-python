from langchain_core.tools import tool

TICKERS = {"YUNextGenAI": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}

@tool(description="Look up the ticker symbol for a company name.")
def get_ticker_symbol(company_name: str):
    return TICKERS[company_name]

@tool(description="Get the current stock price for a ticker symbol.")
def get_stock_price(ticker: str):
    return PRICES[ticker]

print("=== WHAT @tool GENERATED ===")
for t in [get_ticker_symbol, get_stock_price]:
    print(f"TOOL: {t.name}")
    print(f"  description: {t.description}")
    print(f"  args schema: {t.args}")

print()
print("=== THE DAY 30 CHAIN, VIA LANGCHAIN ===")
ticker = get_ticker_symbol.invoke({"company_name": "YUNextGenAI"})
print(f"step 1: YUNextGenAI -> {ticker}")
price = get_stock_price.invoke({"ticker": ticker})
print(f"step 2: {ticker} -> {price}")

print()
print("=== THE FREE VALIDATOR ===")
try:
    get_ticker_symbol.invoke({"wrong_field": "YUNextGenAI"})
except Exception as e:
    print(f"bad input rejected: {e}")