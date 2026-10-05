import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from rag_service import answer_question   # your Project 2 pipeline
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
load_dotenv()

PRICES = {"YNXT": 42.0, "AAPL": 189.5}


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)


@tool(description="Search the Autodesk Revit help docs. Use for any question about Revit features such as walls, doors, or levels.")
def search_revit_docs(question: str) -> str:
    result = answer_question(question)
    print(f"search_revit_docs-> {result.answer}")
    if result.refused or result.answer.strip() == "I don't know.":
        return "NO_MATCH: the Revit docs have nothing relevant to this question."
    return result.answer


TOOLS = [get_price, search_revit_docs]
model = ChatAnthropic(model="claude-opus-4-8", api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools(TOOLS)

SYSTEM = SystemMessage(
    "Prices change — always call get_price for any price question; never reuse an earlier result."
)


class State(TypedDict):
    messages: Annotated[list, add_messages]   # merge rule: APPEND what nodes return


def agent(state: State) -> dict:
    # SYSTEM is prepended on EVERY call but never returned -> never stored in the thread
    print(f"[agent] LLM is receiving {len(state['messages'])} messages")
    response = model_with_tools.invoke([SYSTEM] + state["messages"])
    if response.tool_calls:
        print(f"[agent] tool_calls: {[c['name'] for c in response.tool_calls]}")
    else:
        print(f"[agent] text: {response.content}")
    return {"messages": [response]}


builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
conn = sqlite3.connect("memory.db", check_same_thread=False)   # a file next to where you run it
graph = builder.compile(checkpointer=SqliteSaver(conn))         # = connect-sqlite3 store


def chat(thread_id, text):
    config = {"configurable": {"thread_id": thread_id},   # = the session cookie
              "recursion_limit": 10}                      # loop guard (per turn)
    # send ONLY the new message - the checkpointer LOADs history and SAVEs after
    final = graph.invoke({"messages": [HumanMessage(text)]}, config=config)
    return final


if __name__ == "__main__":
    TURN = 2   # run once with 1, then change to 2 and run again

    TURNS = {
        1: "My ticker is YNXT.",
        2: "What's the price of my ticker?",
    }
    text = TURNS[TURN]
    print(f"===== thread=tushar | TURN {TURN} | {text} =====")
    final = chat("tushar", text)
    print(f"messages in thread: {len(final['messages'])}")