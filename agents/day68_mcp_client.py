import asyncio
import sys

from mcp import Client, StdioServerParameters

# how to START the server: same python, run the server file as a module
SERVER = StdioServerParameters(
    command=sys.executable,
    args=["-m", "agents.day68_mcp_server"])


async def main():
    async with Client(SERVER) as client:          # spawn the server process + connect
        listing = await client.list_tools()       # MCP message: tools/list
        print("tools:", [tool.name for tool in listing.tools])
        result = await client.call_tool("get_entry", {"entry_id": "hero-42"})   # MCP message: tools/call
        print("result:", result.content[0].text)  # the server's answer comes back as a text block
asyncio.run(main())
