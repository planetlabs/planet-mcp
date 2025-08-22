# Planet MCP

planet-mcp is a local [mcp](https://modelcontextprotocol.io/introduction) server powered by the [Planet SDK](https://github.com/planetlabs/planet-client-python). It allows an AI agent/chat to interact with the Planet API using
the Planet CLI.

To get started with your preferred AI agent, find it in the Usage section below.

[TOC]

## Beta warning

**This is experimental software.** This MCP service will invoke the Planet SDK/CLI on your behalf. It can create and modify orders, subscriptions, and more. Do not disable tool approvals. Always carefully review tool prompts before approving them. Use at your own risk.

Tools may be added, removed or altered based on testing/feedback.

It will consume AI tokens.


## Usage (stdio)

#### Prerequisites

1. Python
2. Planet SDK

To install the Planet SDK and `planet-mcp` from the Planet internal PyPI run the following commands:

```
pip install planet
pip install --index-url https://pypi.prod.planet-labs.com/simple/ planet-mcp
```

#### Authentication

You must authenticate your Planet account before using the local MCP server. You can do this by running:

```bash
planet auth login
```

---
**NOTE**

if you have PL_API_KEY set globaly, you should run `unset PL_API_KEY` and then `planet auth reset` and `planet auth login` again.

---

#### Gemini CLI

1. Install [Gemini](https://github.com/google-gemini/gemini-cli)
2. Set up authentication:

   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```
3. Set up gemini by running `gemini` and following the instructions.
4. Quit and add the following to your `~/.gemini/settings.json` file:

   ```json
    "mcpServers": {
      "planet": {
        "command": "planet-mcp",
        "description": "Planet MCP Server",
        "timeout": 30000,
        "trust": false
      }
    }
   ```

#### GitHub Copilot

To allow GitHub Copilot to read these MCP tools, you need to configure the `mcp.json` file. Here's how:

1.  **Locate or create the `mcp.json` file:**

    This file is typically located in here: `/Library/Application Support/Code/User/profiles/-1ccb06ef` If it doesn't exist, you can create it, or create a `.vscode/mcp.json` in your repo.

2.  **Add the following configuration:**

    ```json
    {
      "servers": {
        "planet": {
          "command": "planet-mcp",
        }
      },
      "inputs": []
    }
    ```

#### Claude Code

To use this MCP server with [Claude Code](https://claude.ai/code), run the following command:

```bash
claude mcp add planet planet-mcp
```

This will add the planet-mcp server to your Claude Code configuration, allowing you to interact with Planet's API through Claude Code's terminal interface.



### Example queries

- Does Planet have any recent imagery over Puget Sound?
- List my subscriptions
- Get my June 2025 subscriptions and cancel the ones with name Netherlands
- Create a PlanetScope subscription with the first item in my Netherlands Feature Collection.


## Local dev

### Prerequisites

* python (>= 3.10) + uv
* npx + friends (node >= 20) (to run inspector, if desired)

#### With Makefile

1. ```make dev-up```
2. Optional, `make inspector`

#### Without Makefile

1.  **Create and activate virtual environment using uv:**

    ```bash
    uv venv
    ```
    ```bash
    source .venv/bin/activate
    ```

2.  **Install dependencies using uv:**

    ```bash
    uv pip install -e '.'
    ```

3. **Run mcp server**

    ```bash
    planet-mcp
    ```

Optional run the inspector with
```bash
uv run fastmcp dev src/planet_mcp/main.py
```