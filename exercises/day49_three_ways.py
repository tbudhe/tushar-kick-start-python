import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# ================= PART 0: SETUP (shared by both ways) =================
PRICES = {"YNXT": 42.0, "AAPL": 189.5}          # our fake "database"

@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)
TOOLS = {"get_price": get_price}                 # name Claude says -> function we run

model = ChatAnthropic(model="claude-opus-4-8",
                      api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools([get_price]) # tell Claude the tool exists

QUESTION = "Compare the prices of YNXT and AAPL."

# ================= WAY 1: plain while loop, NO LangGraph =================
print("----- WAY 1: while loop -----")
messages = [HumanMessage(QUESTION)]
while True:
    response = model_with_tools.invoke(messages)          # ask Claude
    messages.append(response)
    if not response.tool_calls:                           # Claude answered -> stop
        print(f"[agent] text: {response.content}")
        break
    print(f"[agent] tool_calls: {[c['name'] for c in response.tool_calls]}")
    for call in response.tool_calls:                      # WE run each tool Claude asked for
        result = TOOLS[call["name"]].invoke(call["args"])
        print(f"[tools] {call['name']}({call['args']['ticker']!r}) --> {result}")
        messages.append(ToolMessage(str(result), tool_call_id=call["id"]))
    # end of loop body -> back to `while True` (= the tools -> agent edge)
print(f"[while loop] {len(messages)} messages")

# ================= WAY 3: LangGraph with PREBUILT pieces =================
print("----- WAY 3: ToolNode -----")

class State(TypedDict):
    messages: Annotated[list, add_messages]   # merge rule: APPEND what nodes return

def agent(state: State) -> dict:
    response = model_with_tools.invoke(state["messages"])  # same call as Way 1
    if response.tool_calls:
        print(f"[agent] tool_calls: {[c['name'] for c in response.tool_calls]}")
    else:
        print(f"[agent] text: {response.content}")
    return {"messages": [response]}           # only the NEW message; add_messages appends it

builder = StateGraph(State)
builder.add_node("agent", agent)                          # your code
builder.add_node("tools", ToolNode([get_price]))          # prebuilt = your Day 48 tools()
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # prebuilt = your should_continue
builder.add_edge("tools", "agent")                        # the backward edge = the while loop
graph = builder.compile()

final = graph.invoke({"messages": [HumanMessage(QUESTION)]},
                     config={"recursion_limit": 10})      # brake: max 10 steps
print(f"[ToolNode] {len(final['messages'])} messages")
