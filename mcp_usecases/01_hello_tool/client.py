from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Needed to run async code
from pathlib import Path  # Helps find server.py in the same folder

from mcp import ClientSession, StdioServerParameters  # MCP session and server launch settings
from mcp.client.stdio import stdio_client  # Connect to MCP server using stdin/stdout

# Find server.py in the same folder as this file
SERVER_SCRIPT = Path(__file__).with_name("server.py")


# Main async function
async def main() -> None:
    # Tell Python how to start the MCP server
    # Same as running: python server.py
    server = StdioServerParameters(
        command="python",
        args=[str(SERVER_SCRIPT)]
    )

    # Start the server and open communication channels
    async with stdio_client(server) as (read, write):

        # Create MCP client session
        async with ClientSession(read, write) as session:

            # Initialize connection between client and server
            await session.initialize()

            # Call the MCP tool named "say_hello"
            # Pass the input name to the tool
            result = await session.call_tool(
                "say_hello",
                {"name": "Giridhar"}
            )

            # Print the response returned by the server
            print(result.content[0].text)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())