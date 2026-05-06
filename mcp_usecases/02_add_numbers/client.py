from __future__ import annotations

import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = Path(__file__).with_name("server.py")

async def main() -> None:
    server = StdioServerParameters(command="python", args=[str(SERVER_SCRIPT)])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("add_numbers", {"a": 10, "b": 25})
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
