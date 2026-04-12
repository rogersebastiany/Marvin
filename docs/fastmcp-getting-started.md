# FastMCP Getting Started


---

## 1. installation

## [​](#install-fastmcp) Install FastMCP

We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to install and manage FastMCP.

```
pip install fastmcp
```

Or with uv:

```
uv add fastmcp
```

### [​](#optional-dependencies) Optional Dependencies

FastMCP provides optional extras for specific features. For example, to install the background tasks extra:

```
pip install "fastmcp[tasks]"
```

See [Background Tasks](/servers/tasks) for details on the task system.

### [​](#verify-installation) Verify Installation

To verify that FastMCP is installed correctly, you can run the following command:

```
fastmcp version
```

You should see output like the following:

```
$ fastmcp version

FastMCP version:                           3.0.0
MCP version:                               1.25.0
Python version:                            3.12.2
Platform:            macOS-15.3.1-arm64-arm-64bit
FastMCP root path:            ~/Developer/fastmcp
```

### [​](#dependency-licensing) Dependency Licensing

FastMCP depends on Cyclopts for CLI functionality. Cyclopts v4 includes docutils as a transitive dependency, which has complex licensing that may trigger compliance reviews in some organizations.If this is a concern, you can install Cyclopts v5 alpha which removes this dependency:

```
pip install "cyclopts>=5.0.0a1"
```

Alternatively, wait for the stable v5 release. See [this issue](https://github.com/BrianPugh/cyclopts/issues/672) for details.

## [​](#upgrading) Upgrading

### [​](#from-fastmcp-2-0) From FastMCP 2.0

See the [Upgrade Guide](/getting-started/upgrading/from-fastmcp-2) for a complete list of breaking changes and migration steps.

### [​](#from-the-mcp-sdk) From the MCP SDK

#### [​](#from-fastmcp-1-0) From FastMCP 1.0

If you’re using FastMCP 1.0 via the `mcp` package (meaning you import FastMCP as `from mcp.server.fastmcp import FastMCP`), upgrading is straightforward — for most servers, it’s a single import change. See the [full upgrade guide](/getting-started/upgrading/from-mcp-sdk) for details.

#### [​](#from-the-low-level-server-api) From the Low-Level Server API

If you built your server directly on the `mcp` package’s `Server` class — with `list_tools()`/`call_tool()` handlers and hand-written JSON Schema — see the [migration guide](/getting-started/upgrading/from-low-level-sdk) for a full walkthrough.

## [​](#versioning-policy) Versioning Policy

FastMCP follows semantic versioning with pragmatic adaptations for the rapidly evolving MCP ecosystem. Breaking changes may occur in minor versions (e.g., 2.3.x to 2.4.0) when necessary to stay current with the MCP Protocol.
For production use, always pin to exact versions:

```
fastmcp==3.0.0  # Good
fastmcp>=3.0.0  # Bad - may install breaking changes
```

See the full [versioning and release policy](/development/releases#versioning-policy) for details on our public API, deprecation practices, and breaking change philosophy.

## [​](#contributing-to-fastmcp) Contributing to FastMCP

Interested in contributing to FastMCP? See the [Contributing Guide](/development/contributing) for details on:

* Setting up your development environment
* Running tests and pre-commit hooks
* Submitting issues and pull requests
* Code standards and review process

---

## 2. quickstart

Welcome! This guide will help you quickly set up FastMCP, run your first MCP server, give it a visual UI, and deploy it to Prefect Horizon.
If you haven’t already installed FastMCP, follow the [installation instructions](/getting-started/installation).

## [​](#create-a-fastmcp-server) Create a FastMCP Server

A FastMCP server is a collection of tools, resources, and other MCP components. To create a server, start by instantiating the `FastMCP` class.
Create a new file called `my_server.py` and add the following code:

my\_server.py

```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

That’s it! You’ve created a FastMCP server, albeit a very boring one. Let’s add a tool to make it more interesting.

## [​](#add-a-tool) Add a Tool

To add a tool that returns a simple greeting, write a function and decorate it with `@mcp.tool` to register it with the server:

my\_server.py

```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## [​](#run-the-server) Run the Server

The simplest way to run your FastMCP server is to call its `run()` method. You can choose between different transports, like `stdio` for local servers, or `http` for remote access:

```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if     mcp.run()
```

This lets us run the server with `python my_server.py`. The stdio transport is the traditional way to connect MCP servers to clients, while the HTTP transport enables remote connections.

Why do we need the `if 
### [​](#using-the-fastmcp-cli) Using the FastMCP CLI

You can also use the `fastmcp run` command to start your server. Note that the FastMCP CLI **does not** execute the `__main__` block of your server file. Instead, it imports your server object and runs it with whatever transport and options you provide.
For example, to run this server with the default stdio transport (no matter how you called `mcp.run()`), you can use the following command:

```
fastmcp run my_server.py:mcp
```

To run this server with the HTTP transport, you can use the following command:

```
fastmcp run my_server.py:mcp --transport http --port 8000
```

## [​](#call-your-server) Call Your Server

Once your server is running with HTTP transport, you can connect to it with a FastMCP client or any LLM client that supports the MCP protocol:

my\_client.py

```
import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))
```

Note that:

* FastMCP clients are asynchronous, so we need to use `asyncio.run` to run the client
* We must enter a client context (`async with client:`) before using the client
* You can make multiple client calls within the same context

## [​](#give-your-tool-a-ui) Give Your Tool a UI

Tools normally return text, but any tool can return an interactive UI instead. Add `app=True` to your tool decorator and return a [Prefab](https://prefab.prefect.io) component — the host renders it as a chart, table, form, or any other visual element right in the conversation. This requires the `apps` extra (`pip install "fastmcp[apps]"`).
The `app=True` flag tells FastMCP to wire up the renderer and protocol metadata automatically. The tool still works like any other MCP tool — it receives arguments and returns a result — but the result is a component tree that the host displays visually instead of as plain text.

my\_server.py

```
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool(app=True)
def greet(name: str) -> PrefabApp:
    """Greet someone with a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Hello, {name}!")
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Greeted", variant="success")

    return PrefabApp(view=view)
```

You can preview app tools locally with `fastmcp dev apps my_server.py` — no MCP host required. See the [Apps overview](/apps/overview) for the full guide, including state management, forms, charts, and server-connected interactivity.

## [​](#deploy-to-prefect-horizon) Deploy to Prefect Horizon

[Prefect Horizon](https://horizon.prefect.io) is the enterprise MCP platform built by the FastMCP team at [Prefect](https://www.prefect.io). It provides managed hosting, authentication, access control, and observability for MCP servers.

Horizon is **free for personal projects** and offers enterprise governance for teams.

To deploy your server, you’ll need a [GitHub account](https://github.com). Once you have one, you can deploy your server in three steps:

1. Push your `my_server.py` file to a GitHub repository
2. Sign in to [Prefect Horizon](https://horizon.prefect.io) with your GitHub account
3. Create a new project from your repository and enter `my_server.py:mcp` as the server entrypoint

That’s it! Horizon will build and deploy your server, making it available at a URL like `https://your-project.fastmcp.app/mcp`. You can chat with it to test its functionality, or connect to it from any LLM client that supports the MCP protocol.
For more details, see the [Prefect Horizon guide](/deployment/prefect-horizon).

---

## 3. welcome

**FastMCP is the standard framework for building MCP applications.** The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) connects LLMs to tools and data. FastMCP gives you everything you need to go from prototype to production — build servers that expose capabilities, connect clients to any MCP service, and give your tools interactive UIs:

```
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if     mcp.run()
```

## [​](#move-fast-and-make-things) Move Fast and Make Things

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) lets you give agents access to your tools and data. But building an effective MCP application is harder than it looks.
FastMCP handles all of it. Declare a tool with a Python function, and the schema, validation, and documentation are generated automatically. Connect to a server with a URL, and transport negotiation, authentication, and protocol lifecycle are managed for you. You focus on your logic, and the MCP part just works: **with FastMCP, best practices are built in.**
**That’s why FastMCP is the standard framework for working with MCP.** FastMCP 1.0 was incorporated into the official MCP Python SDK in 2024. Today, the actively maintained standalone project is downloaded a million times a day, and some version of FastMCP powers 70% of MCP servers across all languages.
FastMCP has three pillars:

## Servers

Expose tools, resources, and prompts to LLMs.

## Apps

Give your tools interactive UIs rendered directly in the conversation.

## Clients

Connect to any MCP server — local or remote, programmatic or CLI.

**[Servers](/servers/server)** wrap your Python functions into MCP-compliant tools, resources, and prompts. **[Clients](/clients/client)** connect to any server with full protocol support. And **[Apps](/apps/overview)** give your tools interactive UIs rendered directly in the conversation.
Ready to build? Start with the [installation guide](/getting-started/installation) or jump straight to the [quickstart](/getting-started/quickstart). When you’re ready to deploy, [Prefect Horizon](https://www.prefect.io/horizon) offers free hosting for FastMCP users.
FastMCP is made with 💙 by [Prefect](https://www.prefect.io/).

**This documentation reflects FastMCP’s `main` branch**, meaning it always reflects the latest development version. Features are generally marked with version badges (e.g. `New in version: 3.0.0`) to indicate when they were introduced. Note that this may include features that are not yet released.

## [​](#llm-friendly-docs) LLM-Friendly Docs

The FastMCP documentation is available in multiple LLM-friendly formats:

### [​](#mcp-server) MCP Server

The FastMCP docs are accessible via MCP! The server URL is `https://gofastmcp.com/mcp`.
In fact, you can use FastMCP to search the FastMCP docs:

```
import asyncio
from fastmcp import Client

async def main():
    async with Client("https://gofastmcp.com/mcp") as client:
        result = await client.call_tool(
            name="SearchFastMcp",
            arguments={"query": "deploy a FastMCP server"}
        )
    print(result)

asyncio.run(main())
```

### [​](#text-formats) Text Formats

The docs are also available in [llms.txt format](https://llmstxt.org/):

* [llms.txt](https://gofastmcp.com/llms.txt) - A sitemap listing all documentation pages
* [llms-full.txt](https://gofastmcp.com/llms-full.txt) - The entire documentation in one file (may exceed context windows)

Any page can be accessed as markdown by appending `.md` to the URL. For example, this page becomes `https://gofastmcp.com/getting-started/welcome.md`.
You can also copy any page as markdown by pressing “Cmd+C” (or “Ctrl+C” on Windows) on your keyboard.

---

## Bibliography

1. [installation](https://gofastmcp.com/getting-started/installation)
2. [quickstart](https://gofastmcp.com/getting-started/quickstart)
3. [welcome](https://gofastmcp.com/getting-started/welcome)