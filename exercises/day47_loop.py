from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    attempts: int   # how many times the work node has run
    done: bool


def work(state: State) -> dict:
    new_count = state["attempts"] + 1              # read the store, add one
    print(f"  [work] attempt {new_count}")         # show each pass
    # only the key this node changed
    return {"attempts": new_count, "done": new_count>=3}


def should_continue(state: State) -> str:
    if state["done"]:                              # did work say it's finished?
        return END                                 # yes: leave the graph
    return "work"                                  # no: go back


builder = StateGraph(State)
builder.add_node("work", work)
builder.add_edge(START, "work")
builder.add_conditional_edges("work", should_continue, {
    "work": "work",
    END: END
})
graph = builder.compile()

if __name__ == "__main__":
    # start the store at 0
    final = graph.invoke({"attempts": 0}, config={"recursion_limit": 10})
    print(f"final state: {final}")                 # what's in the store at END
