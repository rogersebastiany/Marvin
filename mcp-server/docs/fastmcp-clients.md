# FastMCP Clients


---

## 1. In-memory server (ideal for testing)

New in version `2.0.0`
The `fastmcp.Client` class provides a programmatic interface for interacting with any MCP server. It handles protocol details and connection management automatically, letting you focus on the operations you want to perform.
The FastMCP Client is designed for deterministic, controlled interactions rather than autonomous behavior, making it ideal for testing MCP servers during development, building deterministic applications that need reliable MCP interactions, and creating the foundation for agentic or LLM-based clients with structured, type-safe operations.

This is a programmatic client that requires explicit function calls and provides direct control over all MCP operations. Use it as a building block for higher-level systems.

## [​](#creating-a-client) Creating a Client

You provide a server source and the client automatically infers the appropriate transport mechanism.

```
import asyncio
from fastmcp import Client, FastMCP

# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(server)

# HTTP server
client = Client("https://example.com/mcp")

# Local Python script
client = Client("my_mcp_server.py")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        # Execute operations
        result = await client.call_tool("example_tool", {"param": "value"})
        print(result)

asyncio.run(main())
```

All client operations require using the `async with` context manager for proper connection lifecycle management.

## [​](#choosing-a-transport) Choosing a Transport

The client automatically selects a transport based on what you pass to it, but different transports have different characteristics that matter for your use case.
**In-memory transport** connects directly to a FastMCP server instance within the same Python process. Use this for testing and development where you want to eliminate subprocess and network complexity. The server shares your process’s environment and memory space.

```
from fastmcp import Client, FastMCP

server = FastMCP("TestServer")
client = Client(server)  # In-memory, no network or subprocess
```

**STDIO transport** launches a server as a subprocess and communicates through stdin/stdout pipes. This is the standard mechanism used by desktop clients like Claude Desktop. The subprocess runs in an isolated environment, so you must explicitly pass any environment variables the server needs.

```
from fastmcp import Client

# Simple inference from file path
client = Client("my_server.py")

# With explicit environment configuration
client = Client("my_server.py", env={"API_KEY": "secret"})
```

**HTTP transport** connects to servers running as web services. Use this for production deployments where the server runs independently and manages its own lifecycle.

```
from fastmcp import Client

client = Client("https://api.example.com/mcp")
```

See [Transports](/clients/transports) for detailed configuration options including authentication headers, session persistence, and multi-server configurations.

## [​](#configuration-based-clients) Configuration-Based Clients

New in version `2.4.0`
Create clients from MCP configuration dictionaries, which can include multiple servers. While there is no official standard for MCP configuration format, FastMCP follows established conventions used by tools like Claude Desktop.

```
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather-api.example.com/mcp"
        },
        "assistant": {
            "command": "python",
            "args": ["./assistant_server.py"]
        }
    }
}

client = Client(config)

async with client:
    # Tools are prefixed with server names
    weather_data = await client.call_tool("weather_get_forecast", {"city": "London"})
    response = await client.call_tool("assistant_answer_question", {"question": "What's the capital of France?"})

    # Resources use prefixed URIs
    icons = await client.read_resource("weather://weather/icons/sunny")
```

## [​](#connection-lifecycle) Connection Lifecycle

The client uses context managers for connection management. When you enter the context, the client establishes a connection and performs an MCP initialization handshake with the server. This handshake exchanges capabilities, server metadata, and instructions.

```
from fastmcp import Client, FastMCP

mcp = FastMCP(name="MyServer", instructions="Use the greet tool to say hello!")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

async with Client(mcp) as client:
    # Initialization already happened automatically
    print(f"Server: {client.initialize_result.serverInfo.name}")
    print(f"Instructions: {client.initialize_result.instructions}")
    print(f"Capabilities: {client.initialize_result.capabilities.tools}")
```

For advanced scenarios where you need precise control over when initialization happens, disable automatic initialization and call `initialize()` manually:

```
from fastmcp import Client

client = Client("my_mcp_server.py", auto_initialize=False)

async with client:
    # Connection established, but not initialized yet
    print(f"Connected: {client.is_connected()}")
    print(f"Initialized: {client.initialize_result is not None}")  # False

    # Initialize manually with custom timeout
    result = await client.initialize(timeout=10.0)
    print(f"Server: {result.serverInfo.name}")

    # Now ready for operations
    tools = await client.list_tools()
```

## [​](#operations) Operations

FastMCP clients interact with three types of server components.
**Tools** are server-side functions that the client can execute with arguments. Call them with `call_tool()` and receive structured results.

```
async with client:
    tools = await client.list_tools()
    result = await client.call_tool("multiply", {"a": 5, "b": 3})
    print(result.data)  # 15
```

See [Tools](/clients/tools) for detailed documentation including version selection, error handling, and structured output.
**Resources** are data sources that the client can read, either static or templated. Access them with `read_resource()` using URIs.

```
async with client:
    resources = await client.list_resources()
    content = await client.read_resource("file:///config/settings.json")
    print(content[0].text)
```

See [Resources](/clients/resources) for detailed documentation including templates and binary content.
**Prompts** are reusable message templates that can accept arguments. Retrieve rendered prompts with `get_prompt()`.

```
async with client:
    prompts = await client.list_prompts()
    messages = await client.get_prompt("analyze_data", {"data": [1, 2, 3]})
    print(messages.messages)
```

See [Prompts](/clients/prompts) for detailed documentation including argument serialization.

## [​](#callback-handlers) Callback Handlers

The client supports callback handlers for advanced server interactions. These let you respond to server-initiated requests and receive notifications.

```
from fastmcp import Client
from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
    print(f"Server log: {message.data}")

async def progress_handler(progress: float, total: float | None, message: str | None):
    print(f"Progress: {progress}/{total} - {message}")

async def sampling_handler(messages, params, context):
    # Integrate with your LLM service here
    return "Generated response"

client = Client(
    "my_mcp_server.py",
    log_handler=log_handler,
    progress_handler=progress_handler,
    sampling_handler=sampling_handler,
    timeout=30.0
)
```

Each handler type has its own documentation:

* **[Sampling](/clients/sampling)** - Respond to server LLM requests
* **[Elicitation](/clients/elicitation)** - Handle server requests for user input
* **[Progress](/clients/progress)** - Monitor long-running operations
* **[Logging](/clients/logging)** - Handle server log messages
* **[Roots](/clients/roots)** - Provide local context to servers

The FastMCP Client is designed as a foundational tool. Use it directly for deterministic operations, or build higher-level agentic systems on top of its reliable, type-safe interface.

---

## 2. Disable SSL verification (e.g., for self-signed certs in development)

Transports handle the underlying connection between your client and MCP servers. While the client can automatically select a transport based on what you pass to it, instantiating transports explicitly gives you full control over configuration.

## [​](#stdio-transport) STDIO Transport

STDIO transport communicates with MCP servers through subprocess pipes. When using STDIO, your client launches and manages the server process, controlling its lifecycle and environment.

STDIO servers run in isolated environments by default. They do not inherit your shell’s environment variables. You must explicitly pass any configuration the server needs.

```
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

transport = StdioTransport(
    command="python",
    args=["my_server.py", "--verbose"],
    env={"API_KEY": "secret", "LOG_LEVEL": "DEBUG"},
    cwd="/path/to/server"
)
client = Client(transport)
```

For convenience, the client can infer STDIO transport from file paths, though this limits configuration options:

```
from fastmcp import Client

client = Client("my_server.py")  # Limited - no configuration options
```

### [​](#environment-variables) Environment Variables

Since STDIO servers do not inherit your environment, you need strategies for passing configuration.
**Selective forwarding** passes only the variables your server needs:

```
import os
from fastmcp.client.transports import StdioTransport

required_vars = ["API_KEY", "DATABASE_URL", "REDIS_HOST"]
env = {var: os.environ[var] for var in required_vars if var in os.environ}

transport = StdioTransport(command="python", args=["server.py"], env=env)
client = Client(transport)
```

**Loading from .env files** keeps configuration separate from code:

```
from dotenv import dotenv_values
from fastmcp.client.transports import StdioTransport

env = dotenv_values(".env")
transport = StdioTransport(command="python", args=["server.py"], env=env)
client = Client(transport)
```

### [​](#session-persistence) Session Persistence

STDIO transports maintain sessions across multiple client contexts by default (`keep_alive=True`). This reuses the same subprocess for multiple connections, improving performance.

```
from fastmcp.client.transports import StdioTransport

transport = StdioTransport(command="python", args=["server.py"])
client = Client(transport)

async def efficient_multiple_operations():
    async with client:
        await client.ping()

    async with client:  # Reuses the same subprocess
        await client.call_tool("process_data", {"file": "data.csv"})
```

For complete isolation between connections, disable session persistence:

```
transport = StdioTransport(command="python", args=["server.py"], keep_alive=False)
```

## [​](#http-transport) HTTP Transport

HTTP transport connects to MCP servers running as web services. This is the recommended transport for production deployments.

```
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(
    url="https://api.example.com/mcp",
    headers={
        "Authorization": "Bearer your-token-here",
        "X-Custom-Header": "value"
    }
)
client = Client(transport)
```

FastMCP also provides authentication helpers:

```
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

client = Client(
    "https://api.example.com/mcp",
    auth=BearerAuth("your-token-here")
)
```

### [​](#ssl-verification) SSL Verification

By default, HTTPS connections verify the server’s SSL certificate. You can customize this behavior with the `verify` parameter, which accepts the same values as [httpx](https://www.python-httpx.org/advanced/ssl/):

```
from fastmcp import Client

# Disable SSL verification (e.g., for self-signed certs in development)
client = Client("https://dev-server.internal/mcp", verify=False)

# Use a custom CA bundle
client = Client("https://corp-server.internal/mcp", verify="/path/to/ca-bundle.pem")

# Use a custom SSL context for full control
import ssl
ctx = ssl.create_default_context()
ctx.load_verify_locations("/path/to/internal-ca.pem")
client = Client("https://corp-server.internal/mcp", verify=ctx)
```

The `verify` parameter is also available directly on `StreamableHttpTransport` and `SSETransport`:

```
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(
    url="https://dev-server.internal/mcp",
    verify=False,
)
client = Client(transport)
```

### [​](#sse-transport) SSE Transport

Server-Sent Events transport is maintained for backward compatibility. Use Streamable HTTP for new deployments unless you have specific infrastructure requirements.

```
from fastmcp.client.transports import SSETransport

transport = SSETransport(
    url="https://api.example.com/sse",
    headers={"Authorization": "Bearer token"}
)
client = Client(transport)
```

## [​](#in-memory-transport) In-Memory Transport

In-memory transport connects directly to a FastMCP server instance within the same Python process. This eliminates both subprocess management and network overhead, making it ideal for testing.

```
from fastmcp import FastMCP, Client
import os

mcp = FastMCP("TestServer")

@mcp.tool
def greet(name: str) -> str:
    prefix = os.environ.get("GREETING_PREFIX", "Hello")
    return f"{prefix}, {name}!"

client = Client(mcp)

async with client:
    result = await client.call_tool("greet", {"name": "World"})
```

Unlike STDIO transports, in-memory servers share the same memory space and environment variables as your client code.

## [​](#multi-server-configuration) Multi-Server Configuration

Connect to multiple servers defined in a configuration dictionary:

```
from fastmcp import Client

config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather.example.com/mcp",
            "transport": "http"
        },
        "assistant": {
            "command": "python",
            "args": ["./assistant.py"],
            "env": {"LOG_LEVEL": "INFO"}
        }
    }
}

client = Client(config)

async with client:
    # Tools are namespaced by server
    weather = await client.call_tool("weather_get_forecast", {"city": "NYC"})
    answer = await client.call_tool("assistant_ask", {"question": "What?"})
```

### [​](#tool-transformations) Tool Transformations

FastMCP supports tool transformations within the configuration. You can change names, descriptions, tags, and arguments for tools from a server.

```
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather.example.com/mcp",
            "transport": "http",
            "tools": {
                "weather_get_forecast": {
                    "name": "miami_weather",
                    "description": "Get the weather for Miami",
                    "arguments": {
                        "city": {
                            "default": "Miami",
                            "hide": True,
                        }
                    }
                }
            }
        }
    }
}
```

To filter tools by tag, use `include_tags` or `exclude_tags` at the server level:

```
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather.example.com/mcp",
            "include_tags": ["forecast"]  # Only tools with this tag
        }
    }
}
```

---

## Bibliography

1. [In-memory server (ideal for testing)](https://gofastmcp.com/clients/client)
2. [Disable SSL verification (e.g., for self-signed certs in development)](https://gofastmcp.com/clients/transports)