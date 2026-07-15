import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

tools = [
    {
        "name": "get_room_area",
        "description": "Calculate the area of a rectangular room in square feet",
        "input_schema": {
            "type": "object",
            "properties": {
                "length": {"type": "number"},
                "width": {"type": "number"}
            },
            "required": ["length", "width"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=200,
    tools=tools,
    messages=[{"role": "user", "content": "What's the area of a 12x15 room?"}]
)


def get_room_area(length, width):
    return length * width


tool_call = None
for block in response.content:
    if block.type == "tool_use":
        tool_call = block

# actually run it - this is real Python, not the model
result = get_room_area(**tool_call.input)

# Send the result back so the model can use it in its final answer
follow_up = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=200,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the area of a 12x15 room?"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_call.id,
                "content": str(result)}
        ]}
    ]
)

for block in follow_up.content:
    if block.type == "text":
        print(block.text)
