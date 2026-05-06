# Weather Advice

## What this example teaches
Combines weather lookup with advice tool.

## Files
- `main.py` -> run this with MCP Inspector using `mcp dev main.py`
- `server.py` -> MCP server with tools/resources/prompts
- `client.py` -> simple local Python client for direct testing
- `requirements.txt` -> Python dependencies

## Installation

### Option 1: using `uv`
```bash
uv venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate   # Windows
uv pip install -r requirements.txt
```

### Option 2: using `pip`
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Option 3: install with Python directly
```bash
pip install mcp
```

## Run with MCP Inspector
From this example folder:
```bash
mcp dev main.py
```

Alternative:
```bash
npx @modelcontextprotocol/inspector python main.py
```

## Run with the local Python client
```bash
python client.py
```

## Notes
- Do not use `print()` inside `server.py` or `main.py` while the server is running over stdio.
- `client.py` launches `server.py` locally and talks to it over stdio.
- The data in this example is intentionally small and beginner-friendly.

## Typical flow
1. Call `get_weather`\n2. Use output with `suggest_action`\n3. Show combined result

## Expected outcome
Weather plus advice.
