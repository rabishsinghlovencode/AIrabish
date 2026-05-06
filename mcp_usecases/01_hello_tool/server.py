from __future__ import annotations  # Use modern type hint behavior

from typing import Any, Dict, List  # Imported typing helpers (not used in this example)
from mcp.server.fastmcp import FastMCP  # Import FastMCP to create an MCP server

# Create an MCP server and give it a name
mcp = FastMCP("Hello Tool")


# Register this function as an MCP tool
@mcp.tool()
def say_hello(name: str) -> str:
    """Return a friendly greeting."""

    # Return a greeting message using the given name
    return f"Hello, {name}! Welcome to MCP."


# Start the MCP server when this file is run directly
if __name__ == "__main__":
    mcp.run()