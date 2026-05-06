

from __future__ import annotations

import os
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Sentiment Classifier with OpenAI")

# Create OpenAI client
# Make sure OPENAI_API_KEY is set in your environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@mcp.tool()
def classify_sentiment(text: str) -> str:
    """Classify sentiment using an OpenAI model."""

    prompt = f"""
You are a sentiment classifier.

Classify the sentiment of the given text as only one of these:
- positive
- negative
- neutral

Return only one word: positive, negative, or neutral.

Text: {text}
""".strip()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text.strip().lower()


if __name__ == "__main__":
    mcp.run()