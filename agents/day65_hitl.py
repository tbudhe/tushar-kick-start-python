import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

load_dotenv()

PRICES = {"YNXT": 42.0, "AAPL": 189.5}


@tool(description="Get the current stock price for a ticker symbol.")
def get_price(ticker: str):
    return PRICES.get(ticker)


@tool(description="Publish a marketing campaign so it goes live to customers. Irreversible.")
def publish_campaign(name: str):
    # fake - a real one would call Contentful
    return f"PUBLISHED: {name}"


TOOLS = {"get_price": get_price, "publish_campaign": publish_campaign}
# irreversible -> a human must approve
WRITE_TOOLS = {"publish_campaign"}


class State(TypedDict):
    messages: list   # the whole conversation so far


model = ChatAnthropic(model="claude-opus-4-8",
                      api_key=os.getenv("CLAUDE_API_KEY"))
# Claude now knows the tool exists
model_with_tools = model.bind_tools([get_price, publish_campaign])


def agent(state: State) -> dict:
    response = model_with_tools.invoke(state['messages'])
    if response.tool_calls:
        print(
            f"[agent] tool_calls: {[tc['name'] for tc in response.tool_calls]}")
    else:
        print(f"[agent] text: {response.content}")
    return {"messages": state['messages'] + [response]}


def tools(state: State) -> dict:
    last = state["messages"][-1]
    results = []
    for tc in last.tool_calls:
        name, args = tc["name"], tc["args"]
        if name in WRITE_TOOLS:                                   # HITL gate: writes only
            print(f"Agent wants to run: {name}({args})")
            if input("Approve? (y/n) ").strip().lower() != "y":
                # denial is DATA, not an exception
                output = "DENIED: a human rejected this action."
            else:
                output = TOOLS[name].invoke(args)
        else:
            # reads run without asking
            output = TOOLS[name].invoke(args)
        print(f"[tools] {name} --> {output}")
        results.append(ToolMessage(content=str(output), tool_call_id=tc["id"]))
    return {"messages": state["messages"] + results}


def should_continue(state: State) -> str:
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
# THE BACKWARD EDGE: after a tool runs, Claude reads its result
builder.add_edge("tools", "agent")
graph = builder.compile()
if __name__ == "__main__":
    final = graph.invoke(
        {"messages": [HumanMessage("Publish the campaign 'Spring Sale'.")]},
        # our budget: stop after 10 steps, no matter what
        config={"recursion_limit": 10},
    )
    print(f"final: {len(final['messages'])} messages")
