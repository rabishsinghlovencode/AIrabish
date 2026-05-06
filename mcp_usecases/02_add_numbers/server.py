from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Add Numbers")





@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two integers."""
    return a + b



if __name__ == "__main__":
    mcp.run()
