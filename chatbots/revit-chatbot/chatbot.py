import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

system_prompt = "You are a helpful assistant for Autodesk Revit questions. Keep answers short and practical."

conversation = [
    {"role": "user", "content": "How do I add a door in Revit?"},
    {"role": "assistant", "content": "Architecture tab → Door (or press DR). Click a wall to place it. Set position with temporary dimensions."},
    {"role": "user", "content": "How do I change a wall's height?"},
    {"role": "assistant", "content": "Select the wall → Properties panel → set Unconnected Height. Or attach its top to a level."},
]


def ask(user_input):
    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=200,
        system=system_prompt,
        messages=conversation  # send the full history, not just the latest message
    )

    reply = next(
        block.text for block in response.content if block.type == "text")
    # save the reply too
    conversation.append({"role": "assistant", "content": reply})
    return reply


def ask_streaming(user_input):
    conversation.append({"role": "user", "content": user_input})

    full_reply = ""
    with client.messages.stream(
        model="claude-sonnet-5",
        max_tokens=500,
        system=system_prompt,
        messages=conversation
    ) as stream:
        for text_chunk in stream.text_stream:
            # print as it arrives, no newline
            print(text_chunk, end="", flush=True)
            full_reply += text_chunk

    conversation.append({"role": "assistant", "content": full_reply})
    return full_reply


while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    print("Assistant: ", end="")
    ask_streaming(user_input)
    print()
