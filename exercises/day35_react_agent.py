
import os
import inspect
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

TICKERS = {"Yieldnext": "YNXT", "Apple": "AAPL"}
PRICES = {"YNXT": 42.0, "AAPL": 189.5}


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

model = ChatAnthropic(model="claude-haiku-4-5-20251001",
                      api_key=os.getenv("CLAUDE_API_KEY"))
saver = InMemorySaver()
print("=== A: NO checkpointer, one message in ===")
agent_no_check_pointer = create_agent(
    model, [get_ticker, get_price], system_prompt=SYSTEM_PROMPT)
result_agent_no_check_pointer = agent_no_check_pointer.invoke(
    {"messages": [("user", "What's the ticker for that?")]})
for m in result_agent_no_check_pointer["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(
            f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")

print("=== B: WITH checkpointer, thread_id=tushar-1 ===")
agent_check_pointer_thread = create_agent(model, [get_ticker, get_price],
                                          system_prompt=SYSTEM_PROMPT, checkpointer=saver)
cfg_tushar = {"configurable": {"thread_id": "tushar-id-0203"}}
result_agent_check_pointer_thread_1 = agent_check_pointer_thread.invoke(
    {"messages": [("user", "Price of Yieldnext?")]}, config=cfg_tushar)
for m in result_agent_check_pointer_thread_1["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(
            f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")
result_agent_check_pointer_thread_2 = agent_check_pointer_thread.invoke(
    {"messages": [("user", "What's the ticker for that?")]}, config=cfg_tushar)
for m in result_agent_check_pointer_thread_2["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(
            f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")

print("=== C: SAME agent, thread_id=someone-else ===")
cfg_someone_else = {"configurable": {"thread_id": "someone-else"}}
result_agent_check_pointer_someone_else_thread = agent_check_pointer_thread.invoke(
    {"messages": [("user", "What's the ticker for that?")]}, config=cfg_someone_else)
for m in result_agent_check_pointer_someone_else_thread["messages"]:
    label = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(
            f"{label}: tool_calls={[(tc['name'], tc['args']) for tc in m.tool_calls]}")
    else:
        print(f"{label}: {m.content}")

print("=== D: what's actually in the store ===")
def show_store(label, cfg):
    msgs = agent_check_pointer_thread.get_state(cfg).values["messages"]
    has_system = any(isinstance(m, SystemMessage) for m in msgs)
    print(f"{label:22}: {len(msgs)} messages | SystemMessage stored? {has_system}")
show_store("tushar-id-0203", cfg_tushar)
show_store("someone-else", cfg_someone_else)