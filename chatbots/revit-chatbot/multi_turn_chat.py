import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
messages = []  # the conversation store — you own it
MAX_MESSAGES = 4


def trim(messages):
    trimmed = messages[-MAX_MESSAGES:]
    # if trimmed and trimmed[0]["role"] == "assistant":
    #     trimmed = trimmed[1:]  # re-align to start on user
    print(f"[send] {len(trimmed)} msgs, first role = {trimmed[0]['role']}")
    return trimmed


def chat(user_text):
    messages.append({"role": "user", "content": user_text})
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system="You are a Revit expert. Be concise.",
        messages=trim(messages),
    )
    answer = resp.content[0].text
    # save the reply too
    messages.append({"role": "assistant", "content": answer})
    return answer


# print(chat("What is a Revit family?"))
# # "one" only works because history is re-sent
# print(chat("Give me an example of one."))
while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    print("Assistant: ", end="")
    chat_response = chat(user_input)
    print(chat_response)
    print("-------", len(messages))
