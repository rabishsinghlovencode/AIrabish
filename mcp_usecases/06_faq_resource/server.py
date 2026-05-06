from __future__ import annotations  # Modern type hint support

from typing import Any, Dict, List  # Imported typing tools (not used here currently)
from mcp.server.fastmcp import FastMCP  # FastMCP helps create an MCP server easily

# Create an MCP server with a name
mcp = FastMCP("FAQ Resource")

# This is the actual FAQ content that will be returned
FAQ_TEXT = """Q: What are support hours?
A: 9 AM to 6 PM.

Q: What is MCP?
A: A standard way for AI applications to connect with tools, prompts, and resources."""

# Register a resource with URI: docs://faq
@mcp.resource("docs://faq")
def faq_resource() -> str:
    """FAQ text for question answering."""
    return FAQ_TEXT  # Return the FAQ text when client asks for docs://faq

# Start the MCP server
if __name__ == "__main__":
    mcp.run()