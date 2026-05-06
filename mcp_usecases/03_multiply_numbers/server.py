from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Multiply Numbers")





@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b



if __name__ == "__main__":
    mcp.run()
