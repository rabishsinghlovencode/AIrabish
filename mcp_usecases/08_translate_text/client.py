from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Needed to run async code
from pathlib import Path  # Helps find server.py in same folder

from mcp import ClientSession, StdioServerParameters  # MCP session and server setup
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

        # Create an MCP client session
        async with ClientSession(read, write) as session:

            # Initialize connection between client and server
            await session.initialize()

            # Call the MCP tool named "translate_text"
            # Pass input values as a dictionary
            result = await session.call_tool(
                "translate_text",
                {"text": "namaste", "target_language": "english"}
            )

            # Print the tool result returned by server
            print(result.content[0].text)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())