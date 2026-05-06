from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("File Summarizer")

REPORT = """Quarterly training report:
Python sessions were completed on time.
Participant feedback improved after adding more practical labs.
Next quarter will include more MCP and agentic AI content."""

@mcp.resource("docs://report")
def report_resource() -> str:
    return REPORT







if __name__ == "__main__":
    mcp.run()
