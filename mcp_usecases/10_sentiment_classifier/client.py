from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Needed to run async code
from pathlib import Path  # Helps find server.py in the same folder

from mcp import ClientSession, StdioServerParameters  # MCP session and server start settings
from mcp.client.stdio import stdio_client  # Connect to MCP server using stdin/stdout

# Find server.py in the same folder as this file
SERVER_SCRIPT = Path(__file__).with_name("server.py")


# Main async function
async def main() -> None:
    # Tell Python how to start the MCP server
    # Same as running: python server.py
    server = StdioServerParameters(command="python", args=[str(SERVER_SCRIPT)])

    # Start the server and open communication channels
    async with stdio_client(server) as (read, write):

        # Create MCP client session
        async with ClientSession(read, write) as session:

            # Initialize the connection between client and server
            await session.initialize()

            # Call the MCP tool named "classify_sentiment"
            # Pass the input text to the tool
            result = await session.call_tool(
                "classify_sentiment",
                {"text": "The training was excellent and very useful."}
            )

            # Print the result returned by the server
            print(result.content[0].text)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())