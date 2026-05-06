


 
import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv  

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ✅ load .env
load_dotenv()


def extract_json(result: Any) -> dict | None:
    if getattr(result, "structuredContent", None):
        return result.structuredContent

    for content in getattr(result, "content", []):
        text = getattr(content, "text", None)
        if not text:
            continue
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            continue

    return None


def print_raw_result(result: Any) -> None:
    if getattr(result, "structuredContent", None):
        print(json.dumps(result.structuredContent, indent=2))
        return

    found = False
    for content in getattr(result, "content", []):
        text = getattr(content, "text", None)
        if text:
            print(text)
            found = True

    if not found:
        print("No readable output returned.")


async def show_available_tools(session: ClientSession) -> None:
    tools_response = await session.list_tools()

    print("\nAvailable tools:")
    for tool in tools_response.tools:
        print(f"- {tool.name}: {tool.description}")


async def who_am_i(session: ClientSession) -> None:
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    try:
        result = await session.call_tool(
            "search_users",
            {
                "q": username,
                "page": 1,
                "per_page": 5,
            },
        )

        data = extract_json(result)
        if not data:
            print("\nCould not parse response. Raw output:")
            print_raw_result(result)
            return

        users = data.get("items", [])
        if not users:
            print("No users found.")
            return

        exact_match = None
        for user in users:
            if user.get("login", "").lower() == username.lower():
                exact_match = user
                break

        if exact_match:
            print("\nUser found:")
            print(f"Username   : {exact_match.get('login')}")
            print(f"Profile URL: {exact_match.get('html_url')}")
            print(f"Type       : {exact_match.get('type')}")
        else:
            print("\nExact match not found. Closest matches:")
            for user in users:
                print(f"- {user.get('login')} -> {user.get('html_url')}")

    except Exception as exc:
        print(f"Error while searching user: {exc}")


async def list_my_repositories(session: ClientSession) -> None:
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    try:
        result = await session.call_tool(
            "search_repositories",
            {
                "query": f"user:{username}",
                "page": 1,
                "perPage": 20,
            },
        )

        data = extract_json(result)
        if not data:
            print("\nCould not parse response. Raw output:")
            print_raw_result(result)
            return

        repos = data.get("items", [])
        if not repos:
            print("No repositories found.")
            return

        print(f"\nRepositories for {username}:")
        for index, repo in enumerate(repos, start=1):
            print(f"{index}. {repo.get('full_name')}")

    except Exception as exc:
        print(f"Error while listing repositories: {exc}")


async def create_repository(session: ClientSession) -> None:
    repo_name = input("Enter new repository name: ").strip()
    if not repo_name:
        print("Repository name cannot be empty.")
        return

    description = input("Enter repository description: ").strip()
    private_choice = input("Make it private? (y/n): ").strip().lower()
    is_private = private_choice == "y"

    try:
        result = await session.call_tool(
            "create_repository",
            {
                "name": repo_name,
                "description": description,
                "private": is_private,
            },
        )

        print("\nRepository created successfully.")
        data = extract_json(result)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print_raw_result(result)

    except Exception as exc:
        print(f"Error while creating repository: {exc}")


async def create_issue(session: ClientSession) -> None:
    owner = input("Owner username: ").strip()
    repo = input("Repository name: ").strip()
    title = input("Issue title: ").strip()
    body = input("Issue body: ").strip()

    if not owner or not repo or not title:
        print("Owner, repository name, and issue title are required.")
        return

    try:
        result = await session.call_tool(
            "create_issue",
            {
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body,
            },
        )

        print("\nIssue created successfully.")
        data = extract_json(result)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print_raw_result(result)

    except Exception as exc:
        print(f"Error while creating issue: {exc}")


async def create_or_update_file(session: ClientSession) -> None:
    owner = input("Owner username: ").strip()
    repo = input("Repository name: ").strip()
    path = input("File path (example: docs/test.txt): ").strip()
    message = input("Commit message: ").strip()

    if not owner or not repo or not path or not message:
        print("Owner, repository name, file path, and commit message are required.")
        return

    print("Enter file content below. Type END on a new line to finish:")
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    content = "\n".join(lines)

    try:
        result = await session.call_tool(
            "create_or_update_file",
            {
                "owner": owner,
                "repo": repo,
                "path": path,
                "content": content,
                "message": message,
            },
        )

        print("\nFile created/updated successfully.")
        data = extract_json(result)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print_raw_result(result)

    except Exception as exc:
        print(f"Error while creating/updating file: {exc}")


async def main() -> None:
    # ✅ read from .env
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN is not set. "
            "Please set it in .env file."
        )

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            **os.environ,
            "GITHUB_PERSONAL_ACCESS_TOKEN": github_token,
        },
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\nConnected to GitHub MCP successfully.")

            while True:
                print("\n===== GITHUB MCP MENU =====")
                print("1. Who am I")
                print("2. List my repositories")
                print("3. Create repository")
                print("4. Create issue in my repository")
                print("5. Create or update file in a repository")
                print("6. Show available tools")
                print("7. Exit")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    await who_am_i(session)
                elif choice == "2":
                    await list_my_repositories(session)
                elif choice == "3":
                    await create_repository(session)
                elif choice == "4":
                    await create_issue(session)
                elif choice == "5":
                    await create_or_update_file(session)
                elif choice == "6":
                    await show_available_tools(session)
                elif choice == "7":
                    print("Exiting program.")
                    break
                else:
                    print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    asyncio.run(main())
 
 
 