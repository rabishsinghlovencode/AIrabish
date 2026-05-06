from __future__ import annotations  # Modern type hint behavior

from typing import Any, Dict, List  # Imported typing tools (not used here)
from mcp.server.fastmcp import FastMCP  # FastMCP helps create MCP server easily

# Create MCP server with a name
mcp = FastMCP("Word Count")

# Article text stored in a variable
ARTICLE = """MCP is useful for building AI systems that can read data and call tools.
This tiny article exists only to demonstrate reading a resource and passing it into a tool."""

# Create a resource named docs://article
@mcp.resource("docs://article")
def article_resource() -> str:
    return ARTICLE  # Return article text when client asks for it

# Create a tool named count_words
@mcp.tool()
def count_words(text: str) -> int:
    """Count words in text."""
    
    # Split text into words and count non-empty words
    return len([word for word in text.split() if word.strip()])

# Start the MCP server
if __name__ == "__main__":
    mcp.run()