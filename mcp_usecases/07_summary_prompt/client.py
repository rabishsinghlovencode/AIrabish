from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Needed to run async code
from pathlib import Path  # Helps find server.py path

from mcp import ClientSession, StdioServerParameters  # MCP session and server setup
from mcp.client.stdio import stdio_client  # Connect to MCP server using stdio

# Find server.py in the same folder as this file
SERVER_SCRIPT = Path(__file__).with_name("server.py")


# Main async function
async def main() -> None:
    # Tell how to start the MCP server
    # Same like running: python server.py
    server = StdioServerParameters(command="python", args=[str(SERVER_SCRIPT)])

    # Start server and open communication channel
    async with stdio_client(server) as (read, write):

        # Create MCP client session
        async with ClientSession(read, write) as session:

            # Initialize the MCP connection
            await session.initialize()

            # Ask server for the prompt named "summarize_notes"
            # and pass input values for style and length
            prompt = await session.get_prompt(
                "summarize_notes",
                {"style": "bullet", "length": "short"}
            )

            # Print the first prompt message text
            print(prompt.messages[0].content.text)


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())