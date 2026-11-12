import asyncio
import os
import sys

import anthropic
from dotenv import load_dotenv
from mcp import Client, StdioServerParameters

load_dotenv()
claude = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])   # the BRAIN
MODEL = "claude-opus-4-8"

# recipe to START your Day 69 server as a child process (the HANDS)
SERVER = StdioServerParameters(
    command=sys.executable,
    args=["-m", "agents.day69_notes_server"])

QUESTION = "What is my interview line about who calls the tool?"


async def main():
    async with Client(SERVER) as client:
        listing = await client.list_tools()              # tools/list
        claude_tools = [{"name": tool.name,
                         "description": tool.description,
                         "input_schema": tool.input_schema}
                        for tool in listing.tools]

        response = claude.messages.create(               # Claude only DECIDES
            model=MODEL, max_tokens=300, tools=claude_tools,
            messages=[{"role": "user", "content": QUESTION}])

        for block in response.content:
            if block.type == "tool_use":                 # a name + an args dict, nothing ran yet
                print("Claude picked:", block.name, block.input)
                result = await client.call_tool(block.name, block.input)   # MY line runs it
                print("result:", result.content[0].text)

asyncio.run(main())