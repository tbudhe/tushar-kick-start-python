from mcp.server.mcpserver import MCPServer

server = MCPServer("contentful")          # the server's name

# fake Contentful data - same as day67
ENTRIES = {"hero-42": "Design without limits"}


@server.tool()                            # register this function as an MCP tool
def get_entry(entry_id: str) -> str:
    """Read the headline of a Contentful entry by its entry id. Read-only."""
    return ENTRIES.get(entry_id, "NOT FOUND")


if __name__ == "__main__":
    server.run()                          # listen on stdin/stdout for tools/list and tools/call
