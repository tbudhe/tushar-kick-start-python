from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are an Autodesk Revit expert. Answer only questions about Revit. Reply only in this format - Tool: [name], Steps: [steps]. Nothing else.",
    messages=[
        # Few-shot example 1
        {"role": "user", "content": "How do I add a door in Revit?"},
        {"role": "assistant", "content": "Tool: Door\n Steps1: Go through architecture tab click Door,click on a Wall to place it "},  # you write this

        # Few-shot example 2
        {"role": "user", "content": "How do I create a floor in Revit?"},
        {"role": "assistant", "content": "Tool: Floor\nSteps: Go to Architecture tab, click Floor, draw the boundary, click green checkmark."},  # you write this

        # Real question
        {"role": "user", "content": "How do I add a window in Revit?"}
    ]
)

print(response.content[0].text)
