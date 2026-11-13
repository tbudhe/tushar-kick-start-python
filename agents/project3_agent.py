import os
import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from revit_rag.rag_service import answer_question   # Project 2 pipeline

load_dotenv()

PRICES = {"YNXT": 42.0, "AAPL": 189.5}


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)


@tool(description="Search the Autodesk Revit help docs. Use for any question about Revit features such as walls, doors, or levels.")
def search_revit_docs(question: str) -> str:
    result = answer_question(question)
    if result.refused or result.answer.strip() == "I don't know.":
        return "NO_MATCH: the Revit docs have nothing relevant to this question."
    return result.answer


@tool(description="Publish a marketing campaign so it goes live to customers. Irreversible.")
def publish_campaign(name: str):
    return f"PUBLISHED: {name}"   # fake - a real one would call Contentful


TOOLS = {"get_price": get_price,
         "search_revit_docs": search_revit_docs,
         "publish_campaign": publish_campaign}
WRITE_TOOLS = {"publish_campaign"}   # irreversible -> a human must approve

model = ChatAnthropic(model="claude-opus-4-8", api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools(list(TOOLS.values()))

SYSTEM = SystemMessage(
    "Prices change - always call get_price for any price question; never reuse an earlier result. "
    "Use search_revit_docs for any Revit question."
)
class State(TypedDict):
    messages: Annotated[list, add_messages]   # merge rule: APPEND what nodes return

def tools(state: State) -> dict:
    last = state["messages"][-1]
    results = []
    for tc in last.tool_calls:
        name, args = tc["name"], tc["args"]
        if name in WRITE_TOOLS:                       # HITL gate: writes only
            print(f"Agent wants to run: {name}({args})")
            if input("Approve? (y/n) ").strip().lower() != "y":
                output = "DENIED: a human rejected this action."
            else:
                output = TOOLS[name].invoke(args)
        else:
            output = TOOLS[name].invoke(args)         # reads run without asking
        print(f"[tools] {name} --> {output}")
        results.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
    return {"messages": results}
def agent(state: State) -> dict:
    # SYSTEM goes in on every call but is never returned, so it's never stored in the thread
    response = model_with_tools.invoke([SYSTEM] + state["messages"])
    if response.tool_calls:
        print(f"[agent] tool_calls: {[c['name'] for c in response.tool_calls]}")
    else:
        print(f"[agent] text: {response.content}")
    return {"messages": [response]}
def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END


builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", tools)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
builder.add_edge("tools", "agent")   # backward edge: Claude reads the tool result

conn = sqlite3.connect("project3.db", check_same_thread=False)
graph = builder.compile(checkpointer=SqliteSaver(conn))
def chat(thread_id, text):
    config = {"configurable": {"thread_id": thread_id},   # = the session cookie
              "recursion_limit": 10}                      # loop guard per turn
    # send ONLY the new message - the checkpointer loads history and saves after
    return graph.invoke({"messages": [HumanMessage(text)]}, config=config)
if __name__ == "__main__":
    TURNS = [
        "My ticker is YNXT.",
        "What's the price of my ticker?",
        "How do I add a door in Revit?",
        "Publish the campaign 'Spring Sale'.",
    ]
    for i, text in enumerate(TURNS, start=1):
        print(f"===== thread=tushar | TURN {i} | {text} =====")
        final = chat("tushar", text)
    print(f"messages in thread: {len(final['messages'])}")