from pathlib import Path

from mcp.server.mcpserver import MCPServer

server = MCPServer("tushar-ai-learning")
REPO = Path(__file__).resolve().parent.parent     # repo root, one level up from agents/


@server.tool()
def current_day() -> str:
    """Return the current learning day and week from STATUS.md."""
    for line in (REPO / "STATUS.md").read_text().splitlines():
        if line.startswith("Day: "):
            return line
    return "NOT FOUND"


@server.tool()
def interview_line(topic: str) -> str:
    """Find an interview line about a topic in INTERVIEW_LINES.md."""
    for line in (REPO / "INTERVIEW_LINES.md").read_text().splitlines():
        if topic.lower() in line.lower():
            return line.strip()
    return "NOT FOUND"

GET_ENTRY_SCHEMA = {
    "name": "get_entry",
    "description": "Read the headline of a Contentful entry by its entry id. Read-only.",
    "input_schema": {"type": "object",
                     "properties": {"entry_id": {"type": "string"}},
                     "required": ["entry_id"]},
}

if __name__ == "__main__":
    server.run()