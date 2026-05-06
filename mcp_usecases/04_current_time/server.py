from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Current Time")





from datetime import datetime

@mcp.tool()
def get_current_time(label: str = "local") -> str:
    """Return the current local time with a label."""
    return f"{label}: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")



if __name__ == "__main__":
    mcp.run()
