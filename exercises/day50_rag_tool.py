import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from rag_service import answer_question   # your Project 2 pipeline (works: file is at repo root)

load_dotenv()

PRICES = {"YNXT": 42.0, "AAPL": 189.5}

@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)


@tool(description="Search the Autodesk Revit help docs. Use for any question about Revit features such as walls, doors, or levels.")
def search_revit_docs(question: str) -> str:
    result = answer_question(question)
    print(f"search_revit_docs-> {result.answer}")        # probe: what the inner Claude said
    if result.refused or result.answer.strip() == "I don't know.":
        return "NO_MATCH: the Revit docs have nothing relevant to this question."
    return result.answer

TOOLS = [get_price, search_revit_docs]     # ONE list: what Claude sees == what ToolNode runs
model = ChatAnthropic(model="claude-opus-4-8",
                      api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools(TOOLS)


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
builder.add_node("tools", ToolNode(TOOLS))                # prebuilt = your Day 48 tools()
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # prebuilt = your should_continue
builder.add_edge("tools", "agent")                        # the backward edge = the while loop
graph = builder.compile()

if __name__ == "__main__":
    USE_SYSTEM = True          # homework: test the code guard ALONE
    SYSTEM = SystemMessage(
        "For Revit questions, answer ONLY from what search_revit_docs returns. "
        "If it returns \"I don't know\" or NO_MATCH, say the Revit docs don't cover it. "
        "Never fill gaps from your own knowledge."
    )
    for QUESTION in ["How do I create a wall in Revit?", "hi"]:
        print(f"===== Q: {QUESTION} =====")
        msgs = [SYSTEM, HumanMessage(QUESTION)] if USE_SYSTEM else [HumanMessage(QUESTION)]
        final = graph.invoke({"messages": msgs}, config={"recursion_limit": 10})
        print(f"messages: {len(final['messages'])}")
