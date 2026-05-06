from __future__ import annotations  # Modern type hint behavior

from typing import Any, Dict, List  # Imported typing tools (not used here)
from mcp.server.fastmcp import FastMCP  # FastMCP helps create MCP server easily

# Create MCP server with a name
mcp = FastMCP("Translate Text")

# Small demo dictionary for translations
TRANSLATIONS = {
    ("namaste", "english"): "hello",
    ("hello", "hindi"): "namaste",
    ("thanks", "hindi"): "dhanyavaad",
}

# Create a tool named translate_text
@mcp.tool()
def translate_text(text: str, target_language: str) -> str:
    """Translate a few demo words using a small dictionary."""
    
    # Convert input to lowercase and search in dictionary
    return TRANSLATIONS.get(
        (text.lower(), target_language.lower()),
        "translation not found"  # Default if no match exists
    )

# Start the MCP server
if __name__ == "__main__":
    mcp.run()