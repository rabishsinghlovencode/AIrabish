from __future__ import annotations  # Use modern type hint behavior

import asyncio  # Needed for async code
from pathlib import Path  # Helps find server.py path

from mcp import ClientSession, StdioServerParameters  # MCP session and server launch setup
from mcp.client.stdio import stdio_client  # Connect to MCP server using stdin/stdout

# Find server.py in the same folder as this client file
SERVER_SCRIPT = Path(__file__).with_name("server.py")


# Main async function
async def main() -> None:
    # Tell Python how to start the MCP server
    # Same as running: python server.py
    server = StdioServerParameters(command="python", args=[str(SERVER_SCRIPT)])

    # Start the server and open communication channel
    async with stdio_client(server) as (read, write):

        # Create a client session
        async with ClientSession(read, write) as session:

            # Initialize the MCP connection
            await session.initialize()

            # Step 1: Read the article resource from server
            article = await session.read_resource("docs://article")

            # Step 2: Send the article text into the count_words tool
            result = await session.call_tool(
                "count_words",
                {"text": article.contents[0].text}
            )

            # Print the word count returned by the tool
            print(result.content[0].text)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())