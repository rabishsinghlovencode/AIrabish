from __future__ import annotations  # Modern type hint behavior

from typing import Any, Dict, List  # Imported typing tools (not used here)
from mcp.server.fastmcp import FastMCP  # FastMCP helps create MCP server easily

# Create MCP server with a name
mcp = FastMCP("Summary Prompt")

# Notes content stored in a string
NOTES = """MCP supports tools, resources, and prompts.
Tools let the model perform actions.
Resources provide readable context.
Prompts provide reusable instructions."""

# Create a resource named docs://notes
@mcp.resource("docs://notes")
def notes_resource() -> str:
    return NOTES  # Return the notes text when requested


# Create a reusable prompt
@mcp.prompt()
def summarize_notes(style: str = "bullet", length: str = "short") -> str:
    """Reusable summarization prompt."""
    return (
        f"Summarize the notes resource in {style} style with a {length} length. "
        "Focus on tools, resources, and prompts."
    )

# Start the MCP server
if __name__ == "__main__":
    mcp.run()
