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
            csv_text = await session.read_resource("data://sales_csv")
            result = await session.call_tool("get_csv_schema", {"file_text": csv_text.contents[0].text})
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
