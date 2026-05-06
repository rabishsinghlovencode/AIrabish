
from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Change this if your MCP server file has a different name
SERVER_SCRIPT = Path(__file__).with_name("server.py")


def print_menu() -> None:
    print("\n" + "=" * 60)
    print("GitHub MCP Client - Menu")
    print("=" * 60)
    print("1. Get GitHub user info")
    print("2. Create repository")
    print("3. Delete repository")
    print("4. Create file")
    print("5. Update file")
    print("6. Delete file")
    print("7. Exit")
    print("=" * 60)


def get_bool_input(prompt: str) -> bool:
    """Read yes/no input and return boolean."""
    while True:
        value = input(f"{prompt} (yes/no): ").strip().lower()
        if value in ("yes", "y", "true", "1"):
            return True
        if value in ("no", "n", "false", "0"):
            return False
        print("Please enter yes or no.")


def get_user_inputs(choice: str) -> tuple[str, dict[str, Any]] | None:
    """Collect user input based on selected menu option."""
    if choice == "1":
        username = input("Enter GitHub username: ").strip()
        return "git_info", {"username": username}

    elif choice == "2":
        repo_name = input("Enter repository name: ").strip()
        private = get_bool_input("Should the repository be private?")
        description = input("Enter description (optional): ").strip()
        return "create_repo", {
            "repo_name": repo_name,
            "private": private,
            "description": description
        }

    elif choice == "3":
        username = input("Enter GitHub username/owner: ").strip()
        repo_name = input("Enter repository name to delete: ").strip()
        return "delete_repo", {
            "username": username,
            "repo_name": repo_name
        }

    elif choice == "4":
        owner = input("Enter repository owner: ").strip()
        repo = input("Enter repository name: ").strip()
        path = input("Enter file path (example: demo.txt or folder/demo.txt): ").strip()
        print("Enter file content below. Press Enter when done:")
        content = input().rstrip()
        commit_message = input("Enter commit message: ").strip()
        branch = input("Enter branch name [default: main]: ").strip() or "main"

        return "create_file", {
            "owner": owner,
            "repo": repo,
            "path": path,
            "content": content,
            "commit_message": commit_message,
            "branch": branch
        }

    elif choice == "5":
        owner = input("Enter repository owner: ").strip()
        repo = input("Enter repository name: ").strip()
        path = input("Enter file path to update: ").strip()
        print("Enter updated file content below. Press Enter when done:")
        content = input().rstrip()
        sha = input("Enter existing file SHA: ").strip()
        commit_message = input("Enter commit message: ").strip()
        branch = input("Enter branch name [default: main]: ").strip() or "main"

        return "update_file", {
            "owner": owner,
            "repo": repo,
            "path": path,
            "content": content,
            "sha": sha,
            "commit_message": commit_message,
            "branch": branch
        }

    elif choice == "6":
        owner = input("Enter repository owner: ").strip()
        repo = input("Enter repository name: ").strip()
        path = input("Enter file path to delete: ").strip()
        sha = input("Enter file SHA: ").strip()
        commit_message = input("Enter commit message: ").strip()
        branch = input("Enter branch name [default: main]: ").strip() or "main"

        return "delete_file", {
            "owner": owner,
            "repo": repo,
            "path": path,
            "sha": sha,
            "commit_message": commit_message,
            "branch": branch
        }

    elif choice == "7":
        return None

    else:
        print("Invalid choice. Please select a valid option.")
        return "invalid", {}


async def call_tool(tool_name: str, arguments: dict[str, Any]) -> None:
    """Start MCP server via stdio and call the selected tool."""
    server = StdioServerParameters(
        command="python",
        args=[str(SERVER_SCRIPT)]
    )

    try:
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(tool_name, arguments)

                print("\n" + "-" * 60)
                print(f"Result from tool: {tool_name}")
                print("-" * 60)

                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)
                    else:
                        print(item)

                print("-" * 60)

    except Exception as e:
        print(f"\nError while calling tool '{tool_name}': {e}")


async def main() -> None:
    """Main menu loop."""
    print("Starting GitHub MCP interactive client...")

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        selected = get_user_inputs(choice)

        if selected is None:
            print("Exiting client. Goodbye!")
            break

        tool_name, arguments = selected

        if tool_name == "invalid":
            continue

        print("\nArguments being sent:")
        print(json.dumps(arguments, indent=2))

        await call_tool(tool_name, arguments)

        again = input("\nDo you want to perform another operation? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Exiting client. Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())