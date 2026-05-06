

# Gmail Tools with MCP

This project provides a set of Gmail tools using the MCP framework, enabling you to send emails, create drafts, and read mail's label using Google's Gmail API. The tools are registered with `FastMCP` and can be accessed via the MCP CLI.

## Features

- 📤 Send emails through Gmail
- 📝 Create email drafts
- 📬 Read Gmail label information

## Prerequisits

- Python 3.8+
- `uv` for dependency management
- MCP CLI (`mcp[cli]`)
- Gmail API credentials (`client_secret.json`)


## Enable Gmail API and download credentials

- Go to the [Google Cloud Console](https://console.developers.google.com/)
- Create a new project (or use an existing one)
- Enable the **Gmail API**
- Configure the **OAuth consent screen**
- Create **OAuth 2.0 Client IDs**
- Download the `client_secret.json` file and place it in the project root


## Setup

### 1. Change the directory

```bash
cd 07_gmail_server
```

### 2. Install dependencies

```bash
uv init (`if not already initialized.`)
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

> **Note**: If you're not using `uv`, you can also run:
> ```bash
> pip install -r requirements.txt
> ```

## Running the Project

### Development (MCP Inspector)

Use this to test your tools in the MCP Inspector:

```bash
mcp dev main.py
```

### Install for Use with Claude or Other Clients

Use this to make your tools available to Claude or other frontends:

```bash
mcp install main.py
```

> This will install and expose the tools defined with `@mcp.tool()` decorators.

## Usage

### Send an Email
![image](https://github.com/user-attachments/assets/1ecace98-129e-4c3f-a118-e78ad419e5da)


### Create a Draft

![image](https://github.com/user-attachments/assets/282b217d-0edc-4f02-aa84-aa56e75e85ba)


### Read Mail Labels

![image](https://github.com/user-attachments/assets/27f30871-b5f5-4f08-9015-319d9a46c46e)


## Project Structure

```
.
├── main.py                # Script defining Gmail tools
├── client_secret.json     # OAuth credentials (keep private)
├── token.json             # Generated after first login
└── README.md              # Project documentation
```

## Notes

- The script generates and uses `token.json` for storing OAuth tokens.
- **Do not commit `client_secret.json` or `token.json` to version control.**