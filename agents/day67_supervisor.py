import os

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
MODEL = "claude-opus-4-8"

# fake Contentful data - a real tool would call the Contentful API
ENTRIES = {"hero-42": "Design without limits"}


def get_entry(entry_id):
    return ENTRIES.get(entry_id, "NOT FOUND")


def publish_campaign(name):
    return f"PUBLISHED: {name}"


# name -> Python function, so the loop can run whatever Claude asks for
FUNCTIONS = {"get_entry": get_entry, "publish_campaign": publish_campaign}

# what Claude sees: name + description + input shape
GET_ENTRY_SCHEMA = {
    "name": "get_entry",
    "description": "Read the headline of a Contentful entry by its entry id. Read-only.",
    "input_schema": {"type": "object",
                     "properties": {"entry_id": {"type": "string"}},
                     "required": ["entry_id"]},
}
PUBLISH_SCHEMA = {
    "name": "publish_campaign",
    "description": "Publish a marketing campaign so it goes live. Irreversible.",
    "input_schema": {"type": "object",
                     "properties": {"name": {"type": "string"}},
                     "required": ["name"]},
}

def run_agent(agent_name, system, task, tools):
    """One tool loop. A specialist = this loop + its own prompt + its own tools."""
    messages = [{"role": "user", "content": task}]
    for _ in range(5):                                   # step budget (Day 65 guardrail)
        response = client.messages.create(
            model=MODEL, max_tokens=500, system=system,
            tools=tools, messages=messages)
        if response.stop_reason != "tool_use":           # no tool request = final answer
            answer = response.content[0].text
            print(f"[{agent_name}] answer: {answer}")
            return answer
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":                 # Claude asked; MY code runs it
                print(f"[{agent_name}] tool: {block.name}({block.input})")
                output = FUNCTIONS[block.name](**block.input)
                results.append({"type": "tool_result",
                                "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})
    return "Stopped: step budget used up."

ROUTES = {"reader", "publisher"}
ROUTER_SYSTEM = ("You route requests for a marketing copilot. Reply with exactly one word: "
                 "reader (look up or read content) or publisher (publish a campaign).")


def supervisor_route(request):
    response = client.messages.create(
        model=MODEL, max_tokens=5, system=ROUTER_SYSTEM,
        messages=[{"role": "user", "content": request}])
    label = response.content[0].text.strip().lower().strip(".")
    return label if label in ROUTES else "reader"       # unknown -> the SAFE agent


READER_PROMPT = "You read Contentful entries for the marketing team. Be brief."
PUBLISHER_PROMPT = "You publish marketing campaigns. Be brief."
READER_TOOLS = [GET_ENTRY_SCHEMA]        # read-only
PUBLISHER_TOOLS = [PUBLISH_SCHEMA]       # write


def handle(request):
    print(f"\nQ: {request}")
    route = supervisor_route(request)                    # LLM call 1: pick the agent
    print(f"[supervisor] -> {route}")
    if route == "publisher":
        return run_agent("publisher", PUBLISHER_PROMPT, request, PUBLISHER_TOOLS)
    return run_agent("reader", READER_PROMPT, request, READER_TOOLS)


if __name__ == "__main__":
    # skip the supervisor on purpose: send a PUBLISH request straight to the READER
    print("reader tools:", [tool["name"] for tool in READER_TOOLS])
    run_agent("reader", READER_PROMPT,
              "Publish the spring-sale campaign.", READER_TOOLS)