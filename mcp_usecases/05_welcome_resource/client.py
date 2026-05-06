from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Helps run async code
from pathlib import Path  # Helps work with file paths

from mcp import ClientSession, StdioServerParameters  # MCP session and server launch settings
from mcp.client.stdio import stdio_client  # Connect to MCP server using stdin/stdout

# Find server.py in the same folder as this file
SERVER_SCRIPT = Path(__file__).with_name("server.py")


# Main async function
async def main() -> None:
    # Tell Python how to start the MCP server
    # This is same like running: python server.py
    server = StdioServerParameters(
        command="python",
        args=[str(SERVER_SCRIPT)]
    )

    # Start the server and open read/write communication channels
    async with stdio_client(server) as (read, write):

        # Create a client session using the read/write streams
        async with ClientSession(read, write) as session:

            # Initialize the connection (handshake between client and server)
            await session.initialize()

            # Ask the server to give the resource named docs://welcome
            #docs://welcome is a resource URI (identifier) in MCP.
            #Give me the welcome document from the server”
            result = await session.read_resource("docs://welcome")

            # Print the text content returned by the server
            print(result.contents[0].text)


# Run the async main function when this file is executed directly
if __name__ == "__main__":
    asyncio.run(main())