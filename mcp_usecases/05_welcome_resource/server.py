from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Welcome Resource")

WELCOME_TEXT = """Welcome to the sample MCP onboarding project.
Read this resource to understand how resources work.
You can combine resources with prompts and tools later."""

@mcp.resource("docs://welcome")
def welcome_resource() -> str:
    """A welcome text resource."""
    return WELCOME_TEXT







if __name__ == "__main__":
    mcp.run()
