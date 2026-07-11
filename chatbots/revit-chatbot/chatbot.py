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

    reply = response.content[0].text
    # save the reply too
    conversation.append({"role": "assistant", "content": reply})
    return reply


# print(ask("How do I add a door in Revit?"))
# # this call still has the door question in context
# print(ask("What about a window instead?"))

print(ask("Which of those two is faster to place?"))