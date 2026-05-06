from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Markdown To HTML")

MARKDOWN = """# MCP Notes

- Tools perform actions
- Resources provide data
- Prompts provide reusable instructions"""

@mcp.resource("docs://markdown")
def markdown_resource() -> str:
    return MARKDOWN




@mcp.tool()
def markdown_to_html(markdown_text: str) -> str:
    """Convert a tiny subset of markdown to HTML."""
    lines = markdown_text.splitlines()
    html = []
    for line in lines:
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- "):
            html.append(f"<li>{line[2:]}</li>")
        elif line.strip():
            html.append(f"<p>{line}</p>")
    if any(item.startswith("<li>") for item in html):
        items = "".join(item for item in html if item.startswith("<li>"))
        html = [item for item in html if not item.startswith("<li>")] + [f"<ul>{items}</ul>"]
    return "".join(html)



if __name__ == "__main__":
    mcp.run()
