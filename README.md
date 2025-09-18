# Planet MCP

planet-mcp is a local [MCP](https://modelcontextprotocol.io/introduction) server powered by the [Planet SDK](https://github.com/planetlabs/planet-client-python). It allows an AI agent/chat to interact with the Planet API.

To get started with your preferred AI agent, find it in the Usage section below.

## Beta warning

**This is experimental software.** This MCP service will invoke the Planet SDK/CLI on your behalf. It can create and modify orders, subscriptions, and more. Do not disable tool approvals and always carefully review tool prompts before approving them. Use at your own risk.

Tools may be added, removed or altered based on testing/feedback.

Reminder: MCP servers and tools will increase the number of tokens used during interactions with your LLM provider.

We would love to hear back from you after using this, if you have a feature request or find something isn't working please file a [Github issue](https://github.com/planetlabs/planet-mcp/issues/new) for us!
Thanks


## Usage

### Prerequisites

1. Python 3.11 or higher

To install the Planet MCP server, use `pip` or your preferred package manager:

```
pip install planet-mcp
```

This will also install the planet SDK.

### Authentication

You must authenticate your Planet account before using the local MCP server. You can do this by running:

```bash
planet auth login
```

---
**NOTE**

if you have PL_API_KEY set globaly, you should run `unset PL_API_KEY` and then `planet auth reset` and `planet auth login` again.

---

### Supported AI assistants

The following AI agents have been tested with the Planet local MCP. For other agents, refer to their documentation for adding a custom MCP server (the Planet local MCP uses `stdio` transport).

#### Claude Code

To connect with [Claude Code](https://claude.ai/code), run the following command:

```bash
claude mcp add planet planet-mcp
```

#### Gemini CLI

Add the following to your `~/.gemini/settings.json` file:

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

To connect using GitHub Copilot, configure the `mcp.json` file (see [VSCode docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_add-an-mcp-server)) with the following configuration:

```json
{
  "servers": {
    "planet": {
      "command": "planet-mcp"
    }
  },
  "inputs": []
}
```

### Customizing the tools
If you'd like, you can enable or disable specific tools in the MCP server. For example, if you're only working with the orders tooling: You can start the server with just the that enabled:
`--include-tags=orders`

If you want to keep the defaults, but disable a certain tool, you can: `--exclude-tags=destinations`

In order to disable more than one tool you can provide a comma separated list like:
`--exclude-tags=destinations,moasics`

By default, we have disabled download tools and the subscriptions tools, as we have found those tools don't work very well with LLMs at the moment.


## Example queries

- Does Planet have any recent imagery over Puget Sound?
- List my feature collections
- Order me the latest high-res imagery over the Netherlands
- Create a PlanetScope order with the first item in my Netherlands Feature Collection.

## Troubleshooting

### Unable to launch planet-mcp (ENOENT, No such file or directory, etc.):

This is likely due to the `planet-mcp` package being installed to a different Python environment than the one your AI agent is using. The easiest way to resolve this is to run `which planet-mcp` after installing the package, and then copy the full path to your AI agent's MCP configuration. For example, if `which planet-mcp` returns `/home/user/.local/share/virtualenvs/test/bin/planet-mcp`, your config file would look like:

```json
{
  "servers": {
    "planet": {
      "command": "/home/user/.local/share/virtualenvs/test/bin/planet-mcp"
    }
  }
}
```


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
