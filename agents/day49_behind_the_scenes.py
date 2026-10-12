import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
PRICES = {"YNXT": 42.0, "AAPL": 189.5}

@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)

model_with_tools = ChatAnthropic(model="claude-opus-4-8",
                                 api_key=os.getenv("CLAUDE_API_KEY")).bind_tools([get_price])

class State(TypedDict):
    messages: Annotated[list, add_messages]

# INSTRUMENT 1: print what we SEND to Claude (proves the whole list is re-sent)
def agent(state: State) -> dict:
    sent = state["messages"]
    print(f"  [agent] SENDING {len(sent)} messages to Claude: {[m.type for m in sent]}")
    return {"messages": [model_with_tools.invoke(sent)]}

# INSTRUMENT 2: wrap the REAL prebuilt tools_condition and print its decision
def router(state: State) -> Literal["tools", "__end__"]:
    decision = tools_condition(state)
    print(f"  [router] tool_calls in last message? -> {decision!r}")
    return decision

def show(m):                                   # pretty-print one message
    if m.type == "ai" and m.tool_calls:
        for c in m.tool_calls:
            print(f"      ai   asks {c['name']}({c['args']})  id=...{c['id'][-6:]}")
    elif m.type == "tool":
        print(f"      tool answers {m.content!r}  for id=...{m.tool_call_id[-6:]}")
    else:
        print(f"      ai   text: {str(m.content)[:60]!r} ...")

builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode([get_price]))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", router)
builder.add_edge("tools", "agent")
graph = builder.compile()

# stream_mode="updates" = yield after EVERY node, showing only what that node RETURNED
step = 0
for update in graph.stream({"messages": [HumanMessage("Compare the prices of YNXT and AAPL.")]},
                           stream_mode="updates", config={"recursion_limit": 10}):
    for node, output in update.items():
        step += 1
        print(f"STEP {step}: node '{node}' returned:")
        for m in output["messages"]:
            show(m)