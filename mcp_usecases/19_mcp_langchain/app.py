

import asyncio
import os
import streamlit as st
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="SQLite MCP Assistant",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQLite Database Assistant using MCP + LangChain + OpenAI")
st.write("Ask questions about your SQLite database from the browser.")


# -----------------------------
# Load Environment
# -----------------------------
ENV_PATH = r"C:\Users\Administrator\Desktop\programs\mcp_training\mcp_foundation\19_mcp_langchain\.env"
load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()


# -----------------------------
# Model
# -----------------------------
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)


# -----------------------------
# MCP SQLite Server Params
# -----------------------------
server_params = StdioServerParameters(
    command=r"C:\Users\Administrator\.local\bin\uv.exe",
    args=[
        "--directory",
        r"C:\Users\Administrator\Desktop\programs\servers-archived\src\sqlite",
        "run",
        "mcp-server-sqlite",
        "--db-path",
        r"C:\Users\Administrator\Desktop\programs\mcp_training\mcp_foundation\19_mcp_langchain\database.db",
    ],
)


# -----------------------------
# Async MCP Query Function
# -----------------------------
async def ask_database(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            agent = create_agent(model, tools)

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


# -----------------------------
# Streamlit Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display Previous Chat
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Chat Input
# -----------------------------
query = st.chat_input("Ask something about your SQLite database...")

if query:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Processing your database query..."):
            try:
                answer = asyncio.run(ask_database(query))
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg
                    }
                )