

import asyncio
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


load_dotenv(r"C:\Users\Administrator\Desktop\programs\mcp_training\mcp_foundation\19_langchain\.env")
print("Environment variables loaded from .env file")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)

server_params = StdioServerParameters(
    command=r"C:\Users\Administrator\Desktop\programs\mcp_training\mcp_foundation\19_langchain\.venv\Scripts\uv.exe",
    args=[
        "--directory",
        r"C:\Users\Administrator\Desktop\programs\servers-archived\src\sqlite",
        "run",
        "mcp-server-sqlite",
        "--db-path",
        r"C:\Users\Administrator\Desktop\programs\mcp_training\mcp_foundation\19_langchain\database.db",
    ],
)


async def process_query(agent, query):
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )
    return response["messages"][-1].content


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            agent = create_agent(model, tools)

            print("SQLite Database Assistant")
            print("Type 'exit' to quit")

            while True:
                query = input("\nEnter your query: ").strip()

                if query.lower() == "exit":
                    break

                if not query:
                    continue

                print("\nProcessing...\n")

                response = await process_query(agent, query)
                print(f"\nAnswer: {response}")


if __name__ == "__main__":
    asyncio.run(main())