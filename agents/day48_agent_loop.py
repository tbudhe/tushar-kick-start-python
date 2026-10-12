import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

load_dotenv()

PRICES = {"YNXT": 42.0, "AAPL": 189.5}

@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)
TOOLS = {"get_price": get_price}   # name Claude says -> function we run

class State(TypedDict):
    messages: list   # the whole conversation so far


model = ChatAnthropic(model="claude-opus-4-8",
                      api_key=os.getenv("CLAUDE_API_KEY"))
model_with_tools = model.bind_tools([get_price])   # Claude now knows the tool exists

def agent(state:State)-> dict:
    response = model_with_tools.invoke(state['messages'])
    if response.tool_calls:
        print(f"[agent] tool_calls: {[tc['name'] for tc in response.tool_calls]}")
    else:
        print(f"[agent] text: {response.content}")
    return {"messages": state['messages'] + [response]}

def tools(state: State) -> dict:
    last = state["messages"][-1]
    results = []
    for tc in last.tool_calls:
        output = TOOLS[tc["name"]].invoke(tc["args"])
        print(f"[tools] {tc['name']}({tc['args']['ticker']!r})--> {output}")
        results.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
    return {"messages": state["messages"] + results}     # same indent as `for`: runs after ALL tools
def should_continue(state:State) ->str:
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END
builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", tools)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    END: END,
})
builder.add_edge("tools", "agent")      # THE BACKWARD EDGE: after a tool runs, Claude reads its result
graph = builder.compile()
if __name__ == "__main__":
    final = graph.invoke(
        {"messages": [HumanMessage("What is the price of YNXT?")]},
        config={"recursion_limit": 10},       # our budget: stop after 10 steps, no matter what
    )
    print(f"final: {len(final['messages'])} messages")