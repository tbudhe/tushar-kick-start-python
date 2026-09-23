from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from exercises.day46_llm_router import llm_route
from rag_service import answer_question


class State(TypedDict):
    question: str   # input: what the user asked
    route: str      # written by classify: "price" or "docs"
    answer: str     # written by price or docs


def price(state: State) -> dict:
    print("  [price]    answer = $42.00")
    return {"answer": "$42.00"}


def greet(state: State) -> dict:
    print(" [greet]  answer= Hi! Ask me about prices or Revit docs.")
    return {"answer": "Hi! Ask me about prices or Revit docs."}


def docs(state: State) -> dict:
    result = answer_question(state['question'])
    print(f"  [docs]     answer = {result.answer}")
    return {"answer": result.answer}


def classify(state: State) -> dict:
    route = llm_route(state["question"])
    print(f" [classify] route = {route}")
    return {"route": route}


def pick_route(state: State) -> str:
    return state["route"]                         # "price" or "docs"


builder = StateGraph(State)                       # the store's schema
builder.add_node("classify", classify)            # register each node by name
builder.add_node("price", price)
builder.add_node("docs", docs)
builder.add_node("greet", greet)
# every run starts at classify
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", pick_route, {
                              "price": "price", "docs": "docs", "greet": "greet"})
builder.add_edge("price", END)                    # both branches finish
builder.add_edge("docs", END)
builder.add_edge("greet", END)
graph = builder.compile()                         # build-time, done once


if __name__ == "__main__":
    for q in ["What is the price of YNXT?", "How do I add a door in Revit?", "greet, How do I add a door in Revit?"]:
        print(f"Q: {q}")
        graph.invoke({"question": q})             # only question is supplied
