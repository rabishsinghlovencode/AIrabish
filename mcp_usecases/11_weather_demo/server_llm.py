

from __future__ import annotations

import os
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Weather Tool with OpenAI")

# Create OpenAI client (make sure API key is set)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather info using OpenAI model."""

    # Prompt to guide LLM
    prompt = f"""
You are a weather assistant.

Provide a simple current weather description for the city: {city}.

Return in one short sentence only.
""".strip()

    # Call OpenAI model
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text.strip()


# Start MCP server
if __name__ == "__main__":
    mcp.run()