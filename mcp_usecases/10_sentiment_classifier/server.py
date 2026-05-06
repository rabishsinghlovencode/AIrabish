from __future__ import annotations  # Modern type hint behavior

from typing import Any, Dict, List  # Imported typing tools (not used here)
from mcp.server.fastmcp import FastMCP  # FastMCP helps create MCP server easily

# Create MCP server with a name
mcp = FastMCP("Sentiment Classifier")

# Register a tool named classify_sentiment
@mcp.tool()
def classify_sentiment(text: str) -> str:
    """Classify very basic sentiment."""

    # Convert input text to lowercase for easy matching
    value = text.lower()

    # Check if any positive word exists in the text
    if any(word in value for word in ["great", "good", "excellent", "love"]):
        return "positive"

    # Check if any negative word exists in the text
    if any(word in value for word in ["bad", "poor", "hate", "issue"]):
        return "negative"

    # If no known positive or negative words found
    return "neutral"

# Start the MCP server
if __name__ == "__main__":
    mcp.run()