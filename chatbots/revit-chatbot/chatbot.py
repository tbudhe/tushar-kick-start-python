import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

system_prompt = "You are a helpful assistant for Autodesk Revit questions. Keep answers short and practical."

# response = client.messages.create(
#     model="claude-sonnet-5",
#     max_tokens=200,
#     system=system_prompt,
#     messages=[{"role": "user", "content": "How do I add a door in Revit?"}]
# )

# print(response.content[0].text)

conversation = []  # this list IS the memory


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

# print(ask("How do I add a door in Revit?"))
# # # this call still has the door question in context
# print(ask("What about a window instead?"))

# print(ask("Which of those two is faster to place?"))


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

    print()  # newline after streaming finishes
    conversation.append({"role": "assistant", "content": full_reply})
    return full_reply


while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    print("Assistant: ", end="")
    ask_streaming(user_input)
