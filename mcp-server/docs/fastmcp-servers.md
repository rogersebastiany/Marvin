# FastMCP Servers


---

## 1. Run with HTTP transport

The `FastMCP` class is the central piece of every FastMCP application. It acts as the container for your tools, resources, and prompts, managing communication with MCP clients and orchestrating the entire server lifecycle.

## [​](#creating-a-server) Creating a Server

At its simplest, a FastMCP server just needs a name. Everything else has sensible defaults.

```
from fastmcp import FastMCP

mcp = FastMCP("MyServer")
```

Instructions help clients (and the LLMs behind them) understand what your server does and how to use it effectively.

```
mcp = FastMCP(
    "DataAnalysis",
    instructions="Provides tools for analyzing numerical datasets. Start with get_summary() for an overview.",
)
```

## [​](#components) Components

FastMCP servers expose three types of components to clients, each serving a distinct role in the MCP protocol.
**Tools** are functions that clients invoke to perform actions or access external systems.

```
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b
```

**Resources** expose data that clients can read — passive data sources rather than invocable functions.

```
@mcp.resource("data://config")
def get_config() -> dict:
    return {"theme": "dark", "version": "1.0"}
```

**Prompts** are reusable message templates that guide LLM interactions.

```
@mcp.prompt
def analyze_data(data_points: list[float]) -> str:
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"
```

Each component type has detailed documentation: [Tools](/servers/tools), [Resources](/servers/resources) (including [Resource Templates](/servers/resources#resource-templates)), and [Prompts](/servers/prompts).

## [​](#running-the-server) Running the Server

Start your server by calling `mcp.run()`. The `if __name__` guard ensures compatibility with MCP clients that launch your server as a subprocess.

```
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if     mcp.run()
```

FastMCP supports several transports:

* **STDIO** (default): For local integrations and CLI tools
* **HTTP**: For web services using the Streamable HTTP protocol
* **SSE**: Legacy web transport (deprecated)

```
# Run with HTTP transport
mcp.run(transport="http", host="127.0.0.1", port=9000)
```

The server can also be run using the FastMCP CLI. For detailed information on transports and deployment, see [Running Your Server](/deployment/running-server).

## [​](#configuration-reference) Configuration Reference

The `FastMCP` constructor accepts parameters organized into four categories: identity, composition, behavior, and handlers.

### [​](#identity) Identity

These parameters control how your server presents itself to clients.

## 

[​](#param-name)

name

str

default:"FastMCP"

A human-readable name for your server, shown in client applications and logs

[​](#param-instructions)

instructions

str | None

Description of how to interact with this server. Clients surface these instructions to help LLMs understand the server’s purpose and available functionality

[​](#param-version)

version

str | None

Version string for your server. Defaults to the FastMCP library version if not provided

[​](#param-website-url)

website\_url

str | None

URL to a website with more information about your server. Displayed in client applications

[​](#param-icons)

icons

list[Icon] | None

List of icon representations for your server. See [Icons](/servers/icons) for details

### [​](#composition) Composition

These parameters control what your server is built from — its components, middleware, providers, and lifecycle.

## 

[​](#param-tools)

tools

list[Tool | Callable] | None

Tools to register on the server. An alternative to the `@mcp.tool` decorator when you need to add tools programmatically

[​](#param-auth)

auth

OAuthProvider | TokenVerifier | None

Authentication provider for securing HTTP-based transports. See [Authentication](/servers/auth/authentication) for configuration

[​](#param-middleware)

middleware

list[Middleware] | None

[Middleware](/servers/middleware) that intercepts and transforms every MCP message flowing through the server — requests, responses, and notifications in both directions. Use for cross-cutting concerns like logging, error handling, and rate limiting

[​](#param-providers)

providers

list[Provider] | None

[Providers](/servers/providers) that supply tools, resources, and prompts dynamically. Providers are queried at request time, so they can serve components from databases, APIs, or other external sources

[​](#param-transforms)

transforms

list[Transform] | None

Server-level [transforms](/servers/transforms/transforms) to apply to all components. Transforms modify how tools, resources, and prompts are presented to clients — for example, [search transforms](/servers/transforms/tool-search) replace large catalogs with on-demand discovery

[​](#param-lifespan)

lifespan

Lifespan | AsyncContextManager | None

Server-level setup and teardown logic that runs when the server starts and stops. See [Lifespans](/servers/lifespan) for composable lifespans

### [​](#behavior) Behavior

These parameters tune how the server processes requests and communicates with clients.

## 

[​](#param-on-duplicate)

on\_duplicate

Literal["warn", "error", "replace", "ignore"]

default:"warn"

How to handle duplicate component registrations

[​](#param-strict-input-validation)

strict\_input\_validation

bool

default:"False"

When `False` (default), FastMCP uses Pydantic’s flexible validation that coerces compatible inputs (e.g., `"10"` → `10` for int parameters). When `True`, validates inputs against the exact JSON Schema before calling your function, rejecting type mismatches. See [Input Validation Modes](/servers/tools#input-validation-modes) for details

[​](#param-mask-error-details)

mask\_error\_details

bool | None

When `True`, replaces internal error details in tool/resource responses with a generic message to avoid leaking implementation details to clients. Defaults to the `FASTMCP_MASK_ERROR_DETAILS` environment variable

[​](#param-list-page-size)

list\_page\_size

int | None

default:"None"

Maximum items per page for list operations (`tools/list`, `resources/list`, etc.). When `None`, all results are returned in a single response. See [Pagination](/servers/pagination) for details

[​](#param-tasks)

tasks

bool | None

default:"False"

Enable background task support. When `True`, tools and resources can return `CreateTaskResult` to run work asynchronously while the client polls for results

[​](#param-client-log-level)

client\_log\_level

LoggingLevel | None

Default minimum log level for messages sent to MCP clients via `context.log()`. When set, messages below this level are suppressed. Individual clients can override this per-session using the MCP `logging/setLevel` request. One of `"debug"`, `"info"`, `"notice"`, `"warning"`, `"error"`, `"critical"`, `"alert"`, or `"emergency"`

[​](#param-dereference-schemas)

dereference\_schemas

bool

default:"True"

Automatically dereference `$ref` pointers in JSON schemas generated from complex Pydantic models. Most clients require flat schemas without `$ref`, so this should usually stay enabled

### [​](#handlers-and-storage) Handlers and Storage

These parameters provide custom handlers for MCP capabilities and persistent storage for session state.

## 

[​](#param-sampling-handler)

sampling\_handler

SamplingHandler | None

Custom handler for MCP sampling requests (server-initiated LLM calls). See [Sampling](/servers/sampling) for details

[​](#param-sampling-handler-behavior)

sampling\_handler\_behavior

Literal["always", "fallback"] | None

default:"fallback"

When `"fallback"`, the sampling handler is used only when no tool-specific handler exists. When `"always"`, this handler is used for all sampling requests

[​](#param-session-state-store)

session\_state\_store

AsyncKeyValue | None

Persistent key-value store for session state that survives across requests. Defaults to an in-memory store. Provide a custom implementation for persistence across server restarts

## [​](#tag-based-filtering) Tag-Based Filtering

Tags let you categorize components and selectively expose them. This is useful for creating different views of your server for different environments or user types.

```
@mcp.tool(tags={"public", "utility"})
def public_tool() -> str:
    return "This tool is public"

@mcp.tool(tags={"internal", "admin"})
def admin_tool() -> str:
    return "This tool is for admins only"
```

The filtering logic works as follows:

* **Enable with `only=True`**: Switches to allowlist mode — only components with at least one matching tag are exposed
* **Disable**: Components with any matching tag are hidden
* **Precedence**: Later calls override earlier ones, so call `disable` after `enable` to exclude from an allowlist

To ensure a component is never exposed, you can set `enabled=False` on the component itself. See the component-specific documentation for details.

```
# Only expose components tagged with "public"
mcp = FastMCP()
mcp.enable(tags={"public"}, only=True)

# Hide components tagged as "internal" or "deprecated"
mcp = FastMCP()
mcp.disable(tags={"internal", "deprecated"})

# Combine both: show admin tools but hide deprecated ones
mcp = FastMCP()
mcp.enable(tags={"admin"}, only=True).disable(tags={"deprecated"})
```

This filtering applies to all component types (tools, resources, resource templates, and prompts) and affects both listing and access.

## [​](#custom-routes) Custom Routes

When running with HTTP transport, you can add custom web routes alongside your MCP endpoint using the `@custom_route` decorator.

```
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if     mcp.run(transport="http")  # Health check at http://localhost:8000/health
```

Custom routes are useful for health checks, status endpoints, and simple webhooks. For more complex web applications, consider [mounting your MCP server into a FastAPI or Starlette app](/deployment/http#integration-with-web-frameworks).

---

## 2. Utility function that needs context but doesn't receive it as a parameter

When defining FastMCP [tools](/servers/tools), [resources](/servers/resources), resource templates, or [prompts](/servers/prompts), your functions might need to interact with the underlying MCP session or access advanced server capabilities. FastMCP provides the `Context` object for this purpose.

You access Context through FastMCP’s dependency injection system. For other injectable values like HTTP requests, access tokens, and custom dependencies, see [Dependency Injection](/servers/dependency-injection).

## [​](#what-is-context) What Is Context?

The `Context` object provides a clean interface to access MCP features within your functions, including:

* **Logging**: Send debug, info, warning, and error messages back to the client
* **Progress Reporting**: Update the client on the progress of long-running operations
* **Resource Access**: List and read data from resources registered with the server
* **Prompt Access**: List and retrieve prompts registered with the server
* **LLM Sampling**: Request the client’s LLM to generate text based on provided messages
* **User Elicitation**: Request structured input from users during tool execution
* **Session State**: Store data that persists across requests within an MCP session
* **Session Visibility**: [Control which components are visible](/servers/visibility#per-session-visibility) to the current session
* **Request Information**: Access metadata about the current request
* **Server Access**: When needed, access the underlying FastMCP server instance

## [​](#accessing-the-context) Accessing the Context

New in version `2.14`
The preferred way to access context is using the `CurrentContext()` dependency:

```
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context

mcp = FastMCP(name="Context Demo")

@mcp.tool
async def process_file(file_uri: str, ctx: Context = CurrentContext()) -> str:
    """Processes a file, using context for logging and resource access."""
    await ctx.info(f"Processing {file_uri}")
    return "Processed file"
```

This works with tools, resources, and prompts:

```
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context

mcp = FastMCP(name="Context Demo")

@mcp.resource("resource://user-data")
async def get_user_data(ctx: Context = CurrentContext()) -> dict:
    await ctx.debug("Fetching user data")
    return {"user_id": "example"}

@mcp.prompt
async def data_analysis_request(dataset: str, ctx: Context = CurrentContext()) -> str:
    return f"Please analyze the following dataset: {dataset}"
```

**Key Points:**

* Dependency parameters are automatically excluded from the MCP schema—clients never see them.
* Context methods are async, so your function usually needs to be async as well.
* **Each MCP request receives a new context object.** Context is scoped to a single request; state or data set in one request will not be available in subsequent requests.
* Context is only available during a request; attempting to use context methods outside a request will raise errors.

### [​](#legacy-type-hint-injection) Legacy Type-Hint Injection

For backwards compatibility, you can still access context by simply adding a parameter with the `Context` type hint. FastMCP will automatically inject the context instance:

```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.tool
async def process_file(file_uri: str, ctx: Context) -> str:
    """Processes a file, using context for logging and resource access."""
    # Context is injected automatically based on the type hint
    return "Processed file"
```

This approach still works for tools, resources, and prompts. The parameter name doesn’t matter—only the `Context` type hint is important. The type hint can also be a union (`Context | None`) or use `Annotated[]`.

### [​](#via-get_context-function) Via `get_context()` Function

New in version `2.2.11`
For code nested deeper within your function calls where passing context through parameters is inconvenient, use `get_context()` to retrieve the active context from anywhere within a request’s execution flow:

```
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context

mcp = FastMCP(name="Dependency Demo")

# Utility function that needs context but doesn't receive it as a parameter
async def process_data(data: list[float]) -> dict:
    # Get the active context - only works when called within a request
    ctx = get_context()
    await ctx.info(f"Processing {len(data)} data points")

@mcp.tool
async def analyze_dataset(dataset_name: str) -> dict:
    # Call utility function that uses context internally
    data = load_data(dataset_name)
    await process_data(data)
```

**Important Notes:**

* The `get_context()` function should only be used within the context of a server request. Calling it outside of a request will raise a `RuntimeError`.
* The `get_context()` function is server-only and should not be used in client code.

## [​](#context-capabilities) Context Capabilities

FastMCP provides several advanced capabilities through the context object. Each capability has dedicated documentation with comprehensive examples and best practices:

### [​](#logging) Logging

Send debug, info, warning, and error messages back to the MCP client for visibility into function execution.

```
await ctx.debug("Starting analysis")
await ctx.info(f"Processing {len(data)} items")
await ctx.warning("Deprecated parameter used")
await ctx.error("Processing failed")
```

See [Server Logging](/servers/logging) for complete documentation and examples.

### [​](#client-elicitation) Client Elicitation

New in version `2.10.0`
Request structured input from clients during tool execution, enabling interactive workflows and progressive disclosure. This is a new feature in the 6/18/2025 MCP spec.

```
result = await ctx.elicit("Enter your name:", response_type=str)
if result.action == "accept":
    name = result.data
```

See [User Elicitation](/servers/elicitation) for detailed examples and supported response types.

### [​](#llm-sampling) LLM Sampling

New in version `2.0.0`
Request the client’s LLM to generate text based on provided messages, useful for leveraging AI capabilities within your tools.

```
response = await ctx.sample("Analyze this data", temperature=0.7)
```

See [LLM Sampling](/servers/sampling) for comprehensive usage and advanced techniques.

### [​](#progress-reporting) Progress Reporting

Update clients on the progress of long-running operations, enabling progress indicators and better user experience.

```
await ctx.report_progress(progress=50, total=100)  # 50% complete
```

See [Progress Reporting](/servers/progress) for detailed patterns and examples.

### [​](#resource-access) Resource Access

List and read data from resources registered with your FastMCP server, allowing access to files, configuration, or dynamic content.

```
# List available resources
resources = await ctx.list_resources()

# Read a specific resource
content_list = await ctx.read_resource("resource://config")
content = content_list[0].content
```

**Method signatures:**

* **`ctx.list_resources() -> list[MCPResource]`**: New in version `2.13.0` Returns list of all available resources
* **`ctx.read_resource(uri: str | AnyUrl) -> list[ReadResourceContents]`**: Returns a list of resource content parts

### [​](#prompt-access) Prompt Access

New in version `2.13.0`
List and retrieve prompts registered with your FastMCP server, allowing tools and middleware to discover and use available prompts programmatically.

```
# List available prompts
prompts = await ctx.list_prompts()

# Get a specific prompt with arguments
result = await ctx.get_prompt("analyze_data", {"dataset": "users"})
messages = result.messages
```

**Method signatures:**

* **`ctx.list_prompts() -> list[MCPPrompt]`**: Returns list of all available prompts
* **`ctx.get_prompt(name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult`**: Get a specific prompt with optional arguments

### [​](#session-state) Session State

New in version `3.0.0`
Store data that persists across multiple requests within the same MCP session. Session state is automatically keyed by the client’s session, ensuring isolation between different clients.

```
from fastmcp import FastMCP, Context

mcp = FastMCP("stateful-app")

@mcp.tool
async def increment_counter(ctx: Context) -> int:
    """Increment a counter that persists across tool calls."""
    count = await ctx.get_state("counter") or 0
    await ctx.set_state("counter", count + 1)
    return count + 1

@mcp.tool
async def get_counter(ctx: Context) -> int:
    """Get the current counter value."""
    return await ctx.get_state("counter") or 0
```

Each client session has its own isolated state—two different clients calling `increment_counter` will each have their own counter.
**Method signatures:**

* **`await ctx.set_state(key, value, *, serializable=True)`**: Store a value in session state
* **`await ctx.get_state(key)`**: Retrieve a value (returns None if not found)
* **`await ctx.delete_state(key)`**: Remove a value from session state

State methods are async and require `await`. State expires after 1 day to prevent unbounded memory growth.

#### [​](#non-serializable-values) Non-Serializable Values

By default, state values must be JSON-serializable (dicts, lists, strings, numbers, etc.) so they can be persisted across requests. For non-serializable values like HTTP clients or database connections, pass `serializable=False`:

```
@mcp.tool
async def my_tool(ctx: Context) -> str:
    # This object can't be JSON-serialized
    client = SomeHTTPClient(base_url="https://api.example.com")
    await ctx.set_state("client", client, serializable=False)

    # Retrieve it later in the same request
    client = await ctx.get_state("client")
    return await client.fetch("/data")
```

Values stored with `serializable=False` only live for the current MCP request (a single tool call, resource read, or prompt render). They will not be available in subsequent requests within the session.

#### [​](#custom-storage-backends) Custom Storage Backends

By default, session state uses an in-memory store suitable for single-server deployments. For distributed or serverless deployments, provide a custom storage backend:

```
from key_value.aio.stores.redis import RedisStore

# Use Redis for distributed state
mcp = FastMCP("distributed-app", session_state_store=RedisStore(...))
```

Any backend compatible with the [py-key-value-aio](https://github.com/strawgate/py-key-value) `AsyncKeyValue` protocol works. See [Storage Backends](/servers/storage-backends) for more options including Redis, DynamoDB, and MongoDB.

#### [​](#state-during-initialization) State During Initialization

State set during `on_initialize` middleware persists to subsequent tool calls when using the same session object (STDIO, SSE, single-server HTTP). For distributed/serverless HTTP deployments where different machines handle init and tool calls, state is isolated by the `mcp-session-id` header.

### [​](#session-visibility) Session Visibility

New in version `3.0.0`
Tools can customize which components are visible to their current session using `ctx.enable_components()`, `ctx.disable_components()`, and `ctx.reset_visibility()`. These methods apply visibility rules that affect only the calling session, leaving other sessions unchanged. See [Per-Session Visibility](/servers/visibility#per-session-visibility) for complete documentation, filter criteria, and patterns like namespace activation.

### [​](#change-notifications) Change Notifications

New in version `3.0.0`
FastMCP automatically sends list change notifications when components (such as tools, resources, or prompts) are added, removed, enabled, or disabled. In rare cases where you need to manually trigger these notifications, you can use the context’s notification methods:

```
import mcp.types

@mcp.tool
async def custom_tool_management(ctx: Context) -> str:
    """Example of manual notification after custom tool changes."""
    await ctx.send_notification(mcp.types.ToolListChangedNotification())
    await ctx.send_notification(mcp.types.ResourceListChangedNotification())
    await ctx.send_notification(mcp.types.PromptListChangedNotification())
    return "Notifications sent"
```

These methods are primarily used internally by FastMCP’s automatic notification system and most users will not need to invoke them directly.

### [​](#fastmcp-server) FastMCP Server

To access the underlying FastMCP server instance, you can use the `ctx.fastmcp` property:

```
@mcp.tool
async def my_tool(ctx: Context) -> None:
    # Access the FastMCP server instance
    server_name = ctx.fastmcp.name
    ...
```

### [​](#transport) Transport

New in version `3.0.0`
The `ctx.transport` property indicates which transport is being used to run the server. This is useful when your tool needs to behave differently depending on whether the server is running over STDIO, SSE, or Streamable HTTP. For example, you might want to return shorter responses over STDIO or adjust timeout behavior based on transport characteristics.
The transport type is set once when the server starts and remains constant for the server’s lifetime. It returns `None` when called outside of a server context (for example, in unit tests or when running code outside of an MCP request).

```
from fastmcp import FastMCP, Context

mcp = FastMCP("example")

@mcp.tool
def connection_info(ctx: Context) -> str:
    if ctx.transport == "stdio":
        return "Connected via STDIO"
    elif ctx.transport == "sse":
        return "Connected via SSE"
    elif ctx.transport == "streamable-http":
        return "Connected via Streamable HTTP"
    else:
        return "Transport unknown"
```

**Property signature:** `ctx.transport -> Literal["stdio", "sse", "streamable-http"] | None`

### [​](#mcp-request) MCP Request

Access metadata about the current request and client.

```
@mcp.tool
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    return {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id or "Unknown client"
    }
```

**Available Properties:**

* **`ctx.request_id -> str`**: Get the unique ID for the current MCP request
* **`ctx.client_id -> str | None`**: Get the ID of the client making the request, if provided during initialization
* **`ctx.session_id -> str`**: Get the MCP session ID for session-based data sharing. Raises `RuntimeError` if the MCP session is not yet established.

#### [​](#request-context-availability) Request Context Availability

New in version `2.13.1`
The `ctx.request_context` property provides access to the underlying MCP request context, but returns `None` when the MCP session has not been established yet. This typically occurs:

* During middleware execution in the `on_request` hook before the MCP handshake completes
* During the initialization phase of client connections

The MCP request context is distinct from the HTTP request. For HTTP transports, HTTP request data may be available even when the MCP session is not yet established.
To safely access the request context in situations where it may not be available:

```
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_request

mcp = FastMCP(name="Session Aware Demo")

@mcp.tool
async def session_info(ctx: Context) -> dict:
    """Return session information when available."""

    # Check if MCP session is available
    if ctx.request_context:
        # MCP session available - can access MCP-specific attributes
        return {
            "session_id": ctx.session_id,
            "request_id": ctx.request_id,
            "has_meta": ctx.request_context.meta is not None
        }
    else:
        # MCP session not available - use HTTP helpers for request data (if using HTTP transport)
        request = get_http_request()
        return {
            "message": "MCP session not available",
            "user_agent": request.headers.get("user-agent", "Unknown")
        }
```

For HTTP request access that works regardless of MCP session availability (when using HTTP transports), use the [HTTP request helpers](/servers/dependency-injection#http-request) like `get_http_request()` and `get_http_headers()`.

#### [​](#client-metadata) Client Metadata

New in version `2.13.1`
Clients can send contextual information with their requests using the `meta` parameter. This metadata is accessible through `ctx.request_context.meta` and is available for all MCP operations (tools, resources, prompts).
The `meta` field is `None` when clients don’t provide metadata. When provided, metadata is accessible via attribute access (e.g., `meta.user_id`) rather than dictionary access. The structure of metadata is determined by the client making the request.

```
@mcp.tool
def send_email(to: str, subject: str, body: str, ctx: Context) -> str:
    """Send an email, logging metadata about the request."""

    # Access client-provided metadata
    meta = ctx.request_context.meta

    if meta:
        # Meta is accessed as an object with attribute access
        user_id = meta.user_id if hasattr(meta, 'user_id') else None
        trace_id = meta.trace_id if hasattr(meta, 'trace_id') else None

        # Use metadata for logging, observability, etc.
        if trace_id:
            log_with_trace(f"Sending email for user {user_id}", trace_id)

    # Send the email...
    return f"Email sent to {to}"
```

The MCP request is part of the low-level MCP SDK and intended for advanced use cases. Most users will not need to use it directly.

---

## 3. Basic prompt returning a string (converted to user message automatically)

Prompts are reusable message templates that help LLMs generate structured, purposeful responses. FastMCP simplifies defining these templates, primarily using the `@mcp.prompt` decorator.

## [​](#what-are-prompts) What Are Prompts?

Prompts provide parameterized message templates for LLMs. When a client requests a prompt:

1. FastMCP finds the corresponding prompt definition.
2. If it has parameters, they are validated against your function signature.
3. Your function executes with the validated inputs.
4. The generated message(s) are returned to the LLM to guide its response.

This allows you to define consistent, reusable templates that LLMs can use across different clients and contexts.

## [​](#prompts) Prompts

### [​](#the-@prompt-decorator) The `@prompt` Decorator

The most common way to define a prompt is by decorating a Python function. The decorator uses the function name as the prompt’s identifier.

```
from fastmcp import FastMCP
from fastmcp.prompts import Message

mcp = FastMCP(name="PromptServer")

# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"

# Prompt returning multiple messages
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> list[Message]:
    """Generates a conversation for code generation."""
    return [
        Message(f"Write a {language} function that performs the following task: {task_description}"),
        Message("I'll help you write that function.", role="assistant"),
    ]
```

**Key Concepts:**

* **Name:** By default, the prompt name is taken from the function name.
* **Parameters:** The function parameters define the inputs needed to generate the prompt.
* **Inferred Metadata:** By default:
  + Prompt Name: Taken from the function name (`ask_about_topic`).
  + Prompt Description: Taken from the function’s docstring.

Functions with `*args` or `**kwargs` are not supported as prompts. This restriction exists because FastMCP needs to generate a complete parameter schema for the MCP protocol, which isn’t possible with variable argument lists.

#### [​](#decorator-arguments) Decorator Arguments

While FastMCP infers the name and description from your function, you can override these and add additional metadata using arguments to the `@mcp.prompt` decorator:

```
@mcp.prompt(
    name="analyze_data_request",          # Custom prompt name
    description="Creates a request to analyze data with specific parameters",  # Custom description
    tags={"analysis", "data"},            # Optional categorization tags
    meta={"version": "1.1", "author": "data-team"}  # Custom metadata
)
def data_analysis_prompt(
    data_uri: str = Field(description="The URI of the resource containing the data."),
    analysis_type: str = Field(default="summary", description="Type of analysis.")
) -> str:
    """This docstring is ignored when description is provided."""
    return f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
```

## @prompt Decorator Arguments

[​](#param-name)

name

str | None

Sets the explicit prompt name exposed via MCP. If not provided, uses the function name

[​](#param-title)

title

str | None

A human-readable title for the prompt

[​](#param-description)

description

str | None

Provides the description exposed via MCP. If set, the function’s docstring is ignored for this purpose

[​](#param-tags)

tags

set[str] | None

A set of strings used to categorize the prompt. These can be used by the server and, in some cases, by clients to filter or group available prompts.

[​](#param-enabled)

enabled

bool

default:"True"

Deprecated in v3.0.0. Use `mcp.enable()` / `mcp.disable()` at the server level instead.

A boolean to enable or disable the prompt. See [Component Visibility](#component-visibility) for the recommended approach.

[​](#param-icons)

icons

list[Icon] | None

New in version `2.13.0`Optional list of icon representations for this prompt. See [Icons](/servers/icons) for detailed examples

[​](#param-meta)

meta

dict[str, Any] | None

New in version `2.11.0`Optional meta information about the prompt. This data is passed through to the MCP client as the `meta` field of the client-side prompt object and can be used for custom metadata, versioning, or other application-specific purposes.

[​](#param-version)

version

str | int | None

New in version `3.0.0`Optional version identifier for this prompt. See [Versioning](/servers/versioning) for details.

#### [​](#using-with-methods) Using with Methods

For decorating instance or class methods, use the standalone `@prompt` decorator and register the bound method. See [Tools: Using with Methods](/servers/tools#using-with-methods) for the pattern.

### [​](#argument-types) Argument Types

New in version `2.9.0`
The MCP specification requires that all prompt arguments be passed as strings, but FastMCP allows you to use typed annotations for better developer experience. When you use complex types like `list[int]` or `dict[str, str]`, FastMCP:

1. **Automatically converts** string arguments from MCP clients to the expected types
2. **Generates helpful descriptions** showing the exact JSON string format needed
3. **Preserves direct usage** - you can still call prompts with properly typed arguments

Since the MCP specification only allows string arguments, clients need to know what string format to use for complex types. FastMCP solves this by automatically enhancing the argument descriptions with JSON schema information, making it clear to both humans and LLMs how to format their arguments.

```
@mcp.prompt
def analyze_data(
    numbers: list[int],
    metadata: dict[str, str],
    threshold: float
) -> str:
    """Analyze numerical data."""
    avg = sum(numbers) / len(numbers)
    return f"Average: {avg}, above threshold: {avg > threshold}"
```

**MCP clients will call this prompt with string arguments:**

```
{
  "numbers": "[1, 2, 3, 4, 5]",
  "metadata": "{\"source\": \"api\", \"version\": \"1.0\"}",
  "threshold": "2.5"
}
```

**But you can still call it directly with proper types:**

```
# This also works for direct calls
result = await prompt.render({
    "numbers": [1, 2, 3, 4, 5],
    "metadata": {"source": "api", "version": "1.0"},
    "threshold": 2.5
})
```

Keep your type annotations simple when using this feature. Complex nested types or custom classes may not convert reliably from JSON strings. The automatically generated schema descriptions are the only guidance users receive about the expected format.Good choices: `list[int]`, `dict[str, str]`, `float`, `bool`
Avoid: Complex Pydantic models, deeply nested structures, custom classes

### [​](#return-values) Return Values

Prompt functions must return one of these types:

* **`str`**: Sent as a single user message.
* **`list[Message | str]`**: A sequence of messages (a conversation). Strings are auto-converted to user Messages.
* **`PromptResult`**: Full control over messages, description, and metadata. See [PromptResult](#promptresult) below.

```
from fastmcp.prompts import Message

@mcp.prompt
def roleplay_scenario(character: str, situation: str) -> list[Message]:
    """Sets up a roleplaying scenario with initial messages."""
    return [
        Message(f"Let's roleplay. You are {character}. The situation is: {situation}"),
        Message("Okay, I understand. I am ready. What happens next?", role="assistant")
    ]
```

#### [​](#message) Message

New in version `3.0.0`
`Message` provides a user-friendly wrapper for prompt messages with automatic serialization.

```
from fastmcp.prompts import Message

# String content (user role by default)
Message("Hello, world!")

# Explicit role
Message("I can help with that.", role="assistant")

# Auto-serialized to JSON text
Message({"key": "value"})
Message(["item1", "item2"])
```

`Message` accepts two fields:
**`content`** - The message content. Strings pass through directly. Other types (dict, list, BaseModel) are automatically JSON-serialized to text.
**`role`** - The message role, either `"user"` (default) or `"assistant"`.

## Message

[​](#param-content)

content

Any

required

The content data. Strings pass through directly. Other types (dict, list, BaseModel) are automatically JSON-serialized.

[​](#param-role)

role

Literal['user', 'assistant']

default:"user"

The message role.

#### [​](#promptresult) PromptResult

New in version `3.0.0`
`PromptResult` gives you explicit control over prompt responses: multiple messages, roles, and metadata at both the message and result level.

```
from fastmcp import FastMCP
from fastmcp.prompts import PromptResult, Message

mcp = FastMCP(name="PromptServer")

@mcp.prompt
def code_review(code: str) -> PromptResult:
    """Returns a code review prompt with metadata."""
    return PromptResult(
        messages=[
            Message(f"Please review this code:\n\n```\n{code}\n```"),
            Message("I'll analyze this code for issues.", role="assistant"),
        ],
        description="Code review prompt",
        meta={"review_type": "security", "priority": "high"}
    )
```

For simple cases, you can pass a string directly to `PromptResult`:

```
return PromptResult("Please help me with this task")  # auto-converts to single Message
```

## PromptResult

[​](#param-messages)

messages

str | list[Message]

required

Messages to return. Strings are wrapped as a single user Message.

[​](#param-description-1)

description

str | None

Optional description of the prompt result. If not provided, defaults to the prompt’s docstring.

[​](#param-meta-1)

meta

dict[str, Any] | None

Result-level metadata, included in the MCP response’s `_meta` field. Use this for runtime metadata like categorization, priority, or other client-specific data.

The `meta` field in `PromptResult` is for runtime metadata specific to this render response. This is separate from the `meta` parameter in `@mcp.prompt(meta={...})`, which provides static metadata about the prompt definition itself (returned when listing prompts).

You can still return plain `str` or `list[Message | str]` from your prompt functions—`PromptResult` is opt-in for when you need to include metadata.

### [​](#required-vs-optional-parameters) Required vs. Optional Parameters

Parameters in your function signature are considered **required** unless they have a default value.

```
@mcp.prompt
def data_analysis_prompt(
    data_uri: str,                        # Required - no default value
    analysis_type: str = "summary",       # Optional - has default value
    include_charts: bool = False          # Optional - has default value
) -> str:
    """Creates a request to analyze data with specific parameters."""
    prompt = f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
    if include_charts:
        prompt += " Include relevant charts and visualizations."
    return prompt
```

In this example, the client *must* provide `data_uri`. If `analysis_type` or `include_charts` are omitted, their default values will be used.

### [​](#component-visibility) Component Visibility

New in version `3.0.0`
You can control which prompts are enabled for clients using server-level enabled control. Disabled prompts don’t appear in `list_prompts` and can’t be called.

```
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.prompt(tags={"public"})
def public_prompt(topic: str) -> str:
    return f"Discuss: {topic}"

@mcp.prompt(tags={"internal"})
def internal_prompt() -> str:
    return "Internal system prompt"

# Disable specific prompts by key
mcp.disable(keys={"prompt:internal_prompt"})

# Disable prompts by tag
mcp.disable(tags={"internal"})

# Or use allowlist mode - only enable prompts with specific tags
mcp.enable(tags={"public"}, only=True)
```

See [Visibility](/servers/visibility) for the complete visibility control API including key formats, tag-based filtering, and provider-level control.

### [​](#async-prompts) Async Prompts

FastMCP supports both standard (`def`) and asynchronous (`async def`) functions as prompts. Synchronous functions automatically run in a threadpool to avoid blocking the event loop.

```
# Synchronous prompt (runs in threadpool)
@mcp.prompt
def simple_question(question: str) -> str:
    """Generates a simple question to ask the LLM."""
    return f"Question: {question}"

# Asynchronous prompt
@mcp.prompt
async def data_based_prompt(data_id: str) -> str:
    """Generates a prompt based on data that needs to be fetched."""
    # In a real scenario, you might fetch data from a database or API
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/data/{data_id}") as response:
            data = await response.json()
            return f"Analyze this data: {data['content']}"
```

Use `async def` when your prompt function performs I/O operations like network requests or database queries, since async is more efficient than threadpool dispatch.

### [​](#accessing-mcp-context) Accessing MCP Context

New in version `2.2.5`
Prompts can access additional MCP information and features through the `Context` object. To access it, add a parameter to your prompt function with a type annotation of `Context`:

```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="PromptServer")

@mcp.prompt
async def generate_report_request(report_type: str, ctx: Context) -> str:
    """Generates a request for a report."""
    return f"Please create a {report_type} report. Request ID: {ctx.request_id}"
```

For full documentation on the Context object and all its capabilities, see the [Context documentation](/servers/context).

### [​](#notifications) Notifications

New in version `2.9.1`
FastMCP automatically sends `notifications/prompts/list_changed` notifications to connected clients when prompts are added, enabled, or disabled. This allows clients to stay up-to-date with the current prompt set without manually polling for changes.

```
@mcp.prompt
def example_prompt() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_prompt(example_prompt)               # Sends prompts/list_changed notification
mcp.disable(keys={"prompt:example_prompt"})  # Sends prompts/list_changed notification
mcp.enable(keys={"prompt:example_prompt"})   # Sends prompts/list_changed notification
```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.
Clients can handle these notifications using a [message handler](/clients/notifications) to automatically refresh their prompt lists or update their interfaces.

## [​](#server-behavior) Server Behavior

### [​](#duplicate-prompts) Duplicate Prompts

New in version `2.1.0`
You can configure how the FastMCP server handles attempts to register multiple prompts with the same name. Use the `on_duplicate_prompts` setting during `FastMCP` initialization.

```
from fastmcp import FastMCP

mcp = FastMCP(
    name="PromptServer",
    on_duplicate_prompts="error"  # Raise an error if a prompt name is duplicated
)

@mcp.prompt
def greeting(): return "Hello, how can I help you today?"

# This registration attempt will raise a ValueError because
# "greeting" is already registered and the behavior is "error".
# @mcp.prompt
# def greeting(): return "Hi there! What can I do for you?"
```

The duplicate behavior options are:

* `"warn"` (default): Logs a warning, and the new prompt replaces the old one.
* `"error"`: Raises a `ValueError`, preventing the duplicate registration.
* `"replace"`: Silently replaces the existing prompt with the new one.
* `"ignore"`: Keeps the original prompt and ignores the new registration attempt.

## [​](#versioning) Versioning

New in version `3.0.0`
Prompts support versioning, allowing you to maintain multiple implementations under the same name while clients automatically receive the highest version. See [Versioning](/servers/versioning) for complete documentation on version comparison, retrieval, and migration patterns.

---

## 4. Basic dynamic resource returning a string

Resources represent data or files that an MCP client can read, and resource templates extend this concept by allowing clients to request dynamically generated resources based on parameters passed in the URI.
FastMCP simplifies defining both static and dynamic resources, primarily using the `@mcp.resource` decorator.

## [​](#what-are-resources) What Are Resources?

Resources provide read-only access to data for the LLM or client application. When a client requests a resource URI:

1. FastMCP finds the corresponding resource definition.
2. If it’s dynamic (defined by a function), the function is executed.
3. The content (text, JSON, binary data) is returned to the client.

This allows LLMs to access files, database content, configuration, or dynamically generated information relevant to the conversation.

## [​](#resources) Resources

### [​](#the-@resource-decorator) The `@resource` Decorator

The most common way to define a resource is by decorating a Python function. The decorator requires the resource’s unique URI.

```
import json
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Basic dynamic resource returning a string
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message."""
    return "Hello from FastMCP Resources!"

# Resource returning JSON data
@mcp.resource("data://config")
def get_config() -> str:
    """Provides application configuration as JSON."""
    return json.dumps({
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    })
```

**Key Concepts:**

* **URI:** The first argument to `@resource` is the unique URI (e.g., `"resource://greeting"`) clients use to request this data.
* **Lazy Loading:** The decorated function (`get_greeting`, `get_config`) is only executed when a client specifically requests that resource URI via `resources/read`.
* **Inferred Metadata:** By default:
  + Resource Name: Taken from the function name (`get_greeting`).
  + Resource Description: Taken from the function’s docstring.

#### [​](#decorator-arguments) Decorator Arguments

You can customize the resource’s properties using arguments in the `@mcp.resource` decorator:

```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Example specifying metadata
@mcp.resource(
    uri="data://app-status",      # Explicit URI (required)
    name="ApplicationStatus",     # Custom name
    description="Provides the current status of the application.", # Custom description
    mime_type="application/json", # Explicit MIME type
    tags={"monitoring", "status"}, # Categorization tags
    meta={"version": "2.1", "team": "infrastructure"}  # Custom metadata
)
def get_application_status() -> str:
    """Internal function description (ignored if description is provided above)."""
    return json.dumps({"status": "ok", "uptime": 12345, "version": mcp.settings.version})
```

## @resource Decorator Arguments

[​](#param-uri)

uri

str

required

The unique identifier for the resource

[​](#param-name)

name

str | None

A human-readable name. If not provided, defaults to function name

[​](#param-description)

description

str | None

Explanation of the resource. If not provided, defaults to docstring

[​](#param-mime-type)

mime\_type

str | None

Specifies the content type. FastMCP often infers a default like `text/plain` or `application/json`, but explicit is better for non-text types

[​](#param-tags)

tags

set[str] | None

A set of strings used to categorize the resource. These can be used by the server and, in some cases, by clients to filter or group available resources.

[​](#param-enabled)

enabled

bool

default:"True"

Deprecated in v3.0.0. Use `mcp.enable()` / `mcp.disable()` at the server level instead.

A boolean to enable or disable the resource. See [Component Visibility](#component-visibility) for the recommended approach.

[​](#param-icons)

icons

list[Icon] | None

Optional list of icon representations for this resource or template. See [Icons](/servers/icons) for detailed examples

[​](#param-annotations)

annotations

Annotations | dict | None

An optional `Annotations` object or dictionary to add additional metadata about the resource.

Show Annotations attributes

[​](#param-read-only-hint)

readOnlyHint

bool | None

If true, the resource is read-only and does not modify its environment.

[​](#param-idempotent-hint)

idempotentHint

bool | None

If true, reading the resource repeatedly will have no additional effect on its environment.

[​](#param-meta)

meta

dict[str, Any] | None

Optional meta information about the resource. This data is passed through to the MCP client as the `meta` field of the client-side resource object and can be used for custom metadata, versioning, or other application-specific purposes.

[​](#param-version)

version

str | int | None

Optional version identifier for this resource. See [Versioning](/servers/versioning) for details.

#### [​](#using-with-methods) Using with Methods

For decorating instance or class methods, use the standalone `@resource` decorator and register the bound method. See [Tools: Using with Methods](/servers/tools#using-with-methods) for the pattern.

### [​](#return-values) Return Values

Resource functions must return one of three types:

* **`str`**: Sent as `TextResourceContents` (with `mime_type="text/plain"` by default).
* **`bytes`**: Base64 encoded and sent as `BlobResourceContents`. You should specify an appropriate `mime_type` (e.g., `"image/png"`, `"application/octet-stream"`).
* **`ResourceResult`**: Full control over contents, MIME types, and metadata. See [ResourceResult](#resourceresult) below.

To return structured data like dicts or lists, serialize them to JSON strings using `json.dumps()`. This explicit approach ensures your type checker catches errors during development rather than at runtime when a client reads the resource.

#### [​](#resourceresult) ResourceResult

`ResourceResult` gives you explicit control over resource responses: multiple content items, per-item MIME types, and metadata at both the item and result level.

```
from fastmcp import FastMCP
from fastmcp.resources import ResourceResult, ResourceContent

mcp = FastMCP()

@mcp.resource("data://users")
def get_users() -> ResourceResult:
    return ResourceResult(
        contents=[
            ResourceContent(content='[{"id": 1}]', mime_type="application/json"),
            ResourceContent(content="# Users\n...", mime_type="text/markdown"),
        ],
        meta={"total": 1}
    )
```

`ResourceContent` accepts three fields:
**`content`** - The actual resource content. Can be `str` (text content) or `bytes` (binary content). This is the data that will be returned to the client.
**`mime_type`** - Optional MIME type for the content. Defaults to `"text/plain"` for string content and `"application/octet-stream"` for binary content.
**`meta`** - Optional metadata dictionary that will be included in the MCP response’s `meta` field. Use this for runtime metadata like Content Security Policy headers, caching hints, or other client-specific data.
For simple cases, you can pass `str` or `bytes` directly to `ResourceResult`:

```
return ResourceResult("plain text")           # auto-converts to ResourceContent
return ResourceResult(b"\x00\x01\x02")         # binary content
```

## ResourceResult

[​](#param-contents)

contents

str | bytes | list[ResourceContent]

required

Content to return. Strings and bytes are wrapped in a single `ResourceContent`. Use a list of `ResourceContent` for multiple items or custom MIME types.

[​](#param-meta-1)

meta

dict[str, Any] | None

Result-level metadata, included in the MCP response’s `_meta` field.

## ResourceContent

[​](#param-content)

content

Any

required

The content data. Strings and bytes pass through directly. Other types (dict, list, BaseModel) are automatically JSON-serialized.

[​](#param-mime-type-1)

mime\_type

str | None

MIME type. Defaults to `text/plain` for strings, `application/octet-stream` for bytes, `application/json` for serialized objects.

[​](#param-meta-2)

meta

dict[str, Any] | None

Item-level metadata for this specific content.

### [​](#component-visibility) Component Visibility

You can control which resources are enabled for clients using server-level enabled control. Disabled resources don’t appear in `list_resources` and can’t be read.

```
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.resource("data://public", tags={"public"})
def get_public(): return "public"

@mcp.resource("data://secret", tags={"internal"})
def get_secret(): return "secret"

# Disable specific resources by key
mcp.disable(keys={"resource:data://secret"})

# Disable resources by tag
mcp.disable(tags={"internal"})

# Or use allowlist mode - only enable resources with specific tags
mcp.enable(tags={"public"}, only=True)
```

See [Visibility](/servers/visibility) for the complete visibility control API including key formats, tag-based filtering, and provider-level control.

### [​](#accessing-mcp-context) Accessing MCP Context

Resources and resource templates can access additional MCP information and features through the `Context` object. To access it, add a parameter to your resource function with a type annotation of `Context`:

```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://system-status")
async def get_system_status(ctx: Context) -> str:
    """Provides system status information."""
    return json.dumps({
        "status": "operational",
        "request_id": ctx.request_id
    })

@mcp.resource("resource://{name}/details")
async def get_details(name: str, ctx: Context) -> str:
    """Get details for a specific name."""
    return json.dumps({
        "name": name,
        "accessed_at": ctx.request_id
    })
```

For full documentation on the Context object and all its capabilities, see the [Context documentation](/servers/context).

### [​](#async-resources) Async Resources

FastMCP supports both `async def` and regular `def` resource functions. Synchronous functions automatically run in a threadpool to avoid blocking the event loop.
For I/O-bound operations, async functions are more efficient:

```
import aiofiles
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("file:///app/data/important_log.txt", mime_type="text/plain")
async def read_important_log() -> str:
    """Reads content from a specific log file asynchronously."""
    try:
        async with aiofiles.open("/app/data/important_log.txt", mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        return "Log file not found."
```

### [​](#resource-classes) Resource Classes

While `@mcp.resource` is ideal for dynamic content, you can directly register pre-defined resources (like static files or simple text) using `mcp.add_resource()` and concrete `Resource` subclasses.

```
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.resources import FileResource, TextResource, DirectoryResource

mcp = FastMCP(name="DataServer")

# 1. Exposing a static file directly
readme_path = Path("./README.md").resolve()
if readme_path.exists():
    # Use a file:// URI scheme
    readme_resource = FileResource(
        uri=f"file://{readme_path.as_posix()}",
        path=readme_path, # Path to the actual file
        name="README File",
        description="The project's README.",
        mime_type="text/markdown",
        tags={"documentation"}
    )
    mcp.add_resource(readme_resource)

# 2. Exposing simple, predefined text
notice_resource = TextResource(
    uri="resource://notice",
    name="Important Notice",
    text="System maintenance scheduled for Sunday.",
    tags={"notification"}
)
mcp.add_resource(notice_resource)

# 3. Exposing a directory listing
data_dir_path = Path("./app_data").resolve()
if data_dir_path.is_dir():
    data_listing_resource = DirectoryResource(
        uri="resource://data-files",
        path=data_dir_path, # Path to the directory
        name="Data Directory Listing",
        description="Lists files available in the data directory.",
        recursive=False # Set to True to list subdirectories
    )
    mcp.add_resource(data_listing_resource) # Returns JSON list of files
```

**Common Resource Classes:**

* `TextResource`: For simple string content.
* `BinaryResource`: For raw `bytes` content.
* `FileResource`: Reads content from a local file path. Handles text/binary modes, encoding, and lazy reading.
* `HttpResource`: Fetches content from an HTTP(S) URL (requires `httpx`).
* `DirectoryResource`: Lists files in a local directory (returns JSON).
* (`FunctionResource`: Internal class used by `@mcp.resource`).

Use these when the content is static or sourced directly from a file/URL, bypassing the need for a dedicated Python function.

### [​](#notifications) Notifications

FastMCP automatically sends `notifications/resources/list_changed` notifications to connected clients when resources or templates are added, enabled, or disabled. This allows clients to stay up-to-date with the current resource set without manually polling for changes.

```
@mcp.resource("data://example")
def example_resource() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_resource(example_resource)                   # Sends resources/list_changed notification
mcp.disable(keys={"resource:data://example"})        # Sends resources/list_changed notification
mcp.enable(keys={"resource:data://example"})         # Sends resources/list_changed notification
```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.
Clients can handle these notifications using a [message handler](/clients/notifications) to automatically refresh their resource lists or update their interfaces.

### [​](#annotations) Annotations

FastMCP allows you to add specialized metadata to your resources through annotations. These annotations communicate how resources behave to client applications without consuming token context in LLM prompts.
Annotations serve several purposes in client applications:

* Indicating whether resources are read-only or may have side effects
* Describing the safety profile of resources (idempotent vs. non-idempotent)
* Helping clients optimize caching and access patterns

You can add annotations to a resource using the `annotations` parameter in the `@mcp.resource` decorator:

```
@mcp.resource(
    "data://config",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
def get_config() -> str:
    """Get application configuration."""
    return json.dumps({"version": "1.0", "debug": False})
```

FastMCP supports these standard annotations:

| Annotation | Type | Default | Purpose |
| --- | --- | --- | --- |
| `readOnlyHint` | boolean | true | Indicates if the resource only provides data without side effects |
| `idempotentHint` | boolean | true | Indicates if repeated reads have the same effect as a single read |

Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and optimize access patterns, but won’t enforce behavior on their own. Always focus on making your annotations accurately represent what your resource actually does.

## [​](#resource-templates) Resource Templates

Resource Templates allow clients to request resources whose content depends on parameters embedded in the URI. Define a template using the **same `@mcp.resource` decorator**, but include `{parameter_name}` placeholders in the URI string and add corresponding arguments to your function signature.
Resource templates share most configuration options with regular resources (name, description, mime\_type, tags, annotations), but add the ability to define URI parameters that map to function parameters.
Resource templates generate a new resource for each unique set of parameters, which means that resources can be dynamically created on-demand. For example, if the resource template `"user://profile/{name}"` is registered, MCP clients could request `"user://profile/ford"` or `"user://profile/marvin"` to retrieve either of those two user profiles as resources, without having to register each resource individually.

Functions with `*args` are not supported as resource templates. However, unlike tools and prompts, resource templates do support `**kwargs` because the URI template defines specific parameter names that will be collected and passed as keyword arguments.

Here is a complete example that shows how to define two resource templates:

```
import json
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Template URI includes {city} placeholder
@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> str:
    """Provides weather information for a specific city."""
    return json.dumps({
        "city": city.capitalize(),
        "temperature": 22,
        "condition": "Sunny",
        "unit": "celsius"
    })

# Template with multiple parameters and annotations
@mcp.resource(
    "repos://{owner}/{repo}/info",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
def get_repo_info(owner: str, repo: str) -> str:
    """Retrieves information about a GitHub repository."""
    return json.dumps({
        "owner": owner,
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "stars": 120,
        "forks": 48
    })
```

With these two templates defined, clients can request a variety of resources:

* `weather://london/current` → Returns weather for London
* `weather://paris/current` → Returns weather for Paris
* `repos://PrefectHQ/fastmcp/info` → Returns info about the PrefectHQ/fastmcp repository
* `repos://prefecthq/prefect/info` → Returns info about the prefecthq/prefect repository

### [​](#rfc-6570-uri-templates) RFC 6570 URI Templates

FastMCP implements [RFC 6570 URI Templates](https://datatracker.ietf.org/doc/html/rfc6570) for resource templates, providing a standardized way to define parameterized URIs. This includes support for simple expansion, wildcard path parameters, and form-style query parameters.

#### [​](#wildcard-parameters) Wildcard Parameters

Resource templates support wildcard parameters that can match multiple path segments. While standard parameters (`{param}`) only match a single path segment and don’t cross ”/” boundaries, wildcard parameters (`{param*}`) can capture multiple segments including slashes. Wildcards capture all subsequent path segments *up until* the defined part of the URI template (whether literal or another parameter). This allows you to have multiple wildcard parameters in a single URI template.

```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Standard parameter only matches one segment
@mcp.resource("files://{filename}")
def get_file(filename: str) -> str:
    """Retrieves a file by name."""
    # Will only match files://<single-segment>
    return f"File content for: {filename}"

# Wildcard parameter can match multiple segments
@mcp.resource("path://{filepath*}")
def get_path_content(filepath: str) -> str:
    """Retrieves content at a specific path."""
    # Can match path://docs/server/resources.mdx
    return f"Content at path: {filepath}"

# Mixing standard and wildcard parameters
@mcp.resource("repo://{owner}/{path*}/template.py")
def get_template_file(owner: str, path: str) -> dict:
    """Retrieves a file from a specific repository and path, but
    only if the resource ends with `template.py`"""
    # Can match repo://PrefectHQ/fastmcp/src/resources/template.py
    return {
        "owner": owner,
        "path": path + "/template.py",
        "content": f"File at {path}/template.py in {owner}'s repository"
    }
```

Wildcard parameters are useful when:

* Working with file paths or hierarchical data
* Creating APIs that need to capture variable-length path segments
* Building URL-like patterns similar to REST APIs

Note that like regular parameters, each wildcard parameter must still be a named parameter in your function signature, and all required function parameters must appear in the URI template.

#### [​](#query-parameters) Query Parameters

FastMCP supports RFC 6570 form-style query parameters using the `{?param1,param2}` syntax. Query parameters provide a clean way to pass optional configuration to resources without cluttering the path.
Query parameters must be optional function parameters (have default values), while path parameters map to required function parameters. This enforces a clear separation: required data goes in the path, optional configuration in query params.

```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Basic query parameters
@mcp.resource("data://{id}{?format}")
def get_data(id: str, format: str = "json") -> str:
    """Retrieve data in specified format."""
    if format == "xml":
        return f"<data id='{id}' />"
    return f'{{"id": "{id}"}}'

# Multiple query parameters with type coercion
@mcp.resource("api://{endpoint}{?version,limit,offset}")
def call_api(endpoint: str, version: int = 1, limit: int = 10, offset: int = 0) -> dict:
    """Call API endpoint with pagination."""
    return {
        "endpoint": endpoint,
        "version": version,
        "limit": limit,
        "offset": offset,
        "results": fetch_results(endpoint, version, limit, offset)
    }

# Query parameters with wildcards
@mcp.resource("files://{path*}{?encoding,lines}")
def read_file(path: str, encoding: str = "utf-8", lines: int = 100) -> str:
    """Read file with optional encoding and line limit."""
    return read_file_content(path, encoding, lines)
```

**Example requests:**

* `data://123` → Uses default format `"json"`
* `data://123?format=xml` → Uses format `"xml"`
* `api://users?version=2&limit=50` → `version=2, limit=50, offset=0`
* `files://src/main.py?encoding=ascii&lines=50` → Custom encoding and line limit

FastMCP automatically coerces query parameter string values to the correct types based on your function’s type hints (`int`, `float`, `bool`, `str`).
**Query parameters vs. hidden defaults:**
Query parameters expose optional configuration to clients. To hide optional parameters from clients entirely (always use defaults), simply omit them from the URI template:

```
# Clients CAN override max_results via query string
@mcp.resource("search://{query}{?max_results}")
def search_configurable(query: str, max_results: int = 10) -> dict:
    return {"query": query, "limit": max_results}

# Clients CANNOT override max_results (not in URI template)
@mcp.resource("search://{query}")
def search_fixed(query: str, max_results: int = 10) -> dict:
    return {"query": query, "limit": max_results}
```

### [​](#template-parameter-rules) Template Parameter Rules

FastMCP enforces these validation rules when creating resource templates:

1. **Required function parameters** (no default values) must appear in the URI path template
2. **Query parameters** (specified with `{?param}` syntax) must be optional function parameters with default values
3. **All URI template parameters** (path and query) must exist as function parameters

Optional function parameters (those with default values) can be:

* Included as query parameters (`{?param}`) - clients can override via query string
* Omitted from URI template - always uses default value, not exposed to clients
* Used in alternative path templates - enables multiple ways to access the same resource

**Multiple templates for one function:**
Create multiple resource templates that expose the same function through different URI patterns by manually applying decorators:

```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Define a user lookup function that can be accessed by different identifiers
def lookup_user(name: str | None = None, email: str | None = None) -> dict:
    """Look up a user by either name or email."""
    if email:
        return find_user_by_email(email)  # pseudocode
    elif name:
        return find_user_by_name(name)  # pseudocode
    else:
        return {"error": "No lookup parameters provided"}

# Manually apply multiple decorators to the same function
mcp.resource("users://email/{email}")(lookup_user)
mcp.resource("users://name/{name}")(lookup_user)
```

Now an LLM or client can retrieve user information in two different ways:

* `users://email/alice@example.com` → Looks up user by email (with name=None)
* `users://name/Bob` → Looks up user by name (with email=None)

This approach allows a single function to be registered with multiple URI patterns while keeping the implementation clean and straightforward.
Templates provide a powerful way to expose parameterized data access points following REST-like principles.

## [​](#error-handling) Error Handling

If your resource function encounters an error, you can raise a standard Python exception (`ValueError`, `TypeError`, `FileNotFoundError`, custom exceptions, etc.) or a FastMCP `ResourceError`.
By default, all exceptions (including their details) are logged and converted into an MCP error response to be sent back to the client LLM. This helps the LLM understand failures and react appropriately.
If you want to mask internal error details for security reasons, you can:

1. Use the `mask_error_details=True` parameter when creating your `FastMCP` instance:

```
mcp = FastMCP(name="SecureServer", mask_error_details=True)
```

2. Or use `ResourceError` to explicitly control what error information is sent to clients:

```
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://safe-error")
def fail_with_details() -> str:
    """This resource provides detailed error information."""
    # ResourceError contents are always sent back to clients,
    # regardless of mask_error_details setting
    raise ResourceError("Unable to retrieve data: file not found")

@mcp.resource("resource://masked-error")
def fail_with_masked_details() -> str:
    """This resource masks internal error details when mask_error_details=True."""
    # This message would be masked if mask_error_details=True
    raise ValueError("Sensitive internal file path: /etc/secrets.conf")

@mcp.resource("data://{id}")
def get_data_by_id(id: str) -> dict:
    """Template resources also support the same error handling pattern."""
    if id == "secure":
        raise ValueError("Cannot access secure data")
    elif id == "missing":
        raise ResourceError("Data ID 'missing' not found in database")
    return {"id": id, "value": "data"}
```

When `mask_error_details=True`, only error messages from `ResourceError` will include details, other exceptions will be converted to a generic message.

## [​](#server-behavior) Server Behavior

### [​](#duplicate-resources) Duplicate Resources

You can configure how the FastMCP server handles attempts to register multiple resources or templates with the same URI. Use the `on_duplicate_resources` setting during `FastMCP` initialization.

```
from fastmcp import FastMCP

mcp = FastMCP(
    name="ResourceServer",
    on_duplicate_resources="error" # Raise error on duplicates
)

@mcp.resource("data://config")
def get_config_v1(): return {"version": 1}

# This registration attempt will raise a ValueError because
# "data://config" is already registered and the behavior is "error".
# @mcp.resource("data://config")
# def get_config_v2(): return {"version": 2}
```

The duplicate behavior options are:

* `"warn"` (default): Logs a warning, and the new resource/template replaces the old one.
* `"error"`: Raises a `ValueError`, preventing the duplicate registration.
* `"replace"`: Silently replaces the existing resource/template with the new one.
* `"ignore"`: Keeps the original resource/template and ignores the new registration attempt.

## [​](#versioning) Versioning

Resources and resource templates support versioning, allowing you to maintain multiple implementations under the same URI while clients automatically receive the highest version. See [Versioning](/servers/versioning) for complete documentation on version comparison, retrieval, and migration patterns.

---

## 5. Limit all tool responses to 500KB

Middleware adds behavior that applies across multiple operations—authentication, logging, rate limiting, or request transformation—without modifying individual tools or resources.

MCP middleware is a FastMCP-specific concept and is not part of the official MCP protocol specification.

## [​](#overview) Overview

MCP middleware forms a pipeline around your server’s operations. When a request arrives, it flows through each middleware in order—each can inspect, modify, or reject the request before passing it along. After the operation completes, the response flows back through the same middleware in reverse order.

```
Request → Middleware A → Middleware B → Handler → Middleware B → Middleware A → Response
```

This bidirectional flow means middleware can:

* **Pre-process**: Validate authentication, log incoming requests, check rate limits
* **Post-process**: Transform responses, record timing metrics, handle errors consistently

The key decision point is `call_next(context)`. Calling it continues the chain; not calling it stops processing entirely.

```
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        print(f"→ {context.method}")
        result = await call_next(context)
        print(f"← {context.method}")
        return result

mcp = FastMCP("MyServer")
mcp.add_middleware(LoggingMiddleware())
```

### [​](#execution-order) Execution Order

Middleware executes in the order added to the server. The first middleware runs first on the way in and last on the way out:

```
from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(ErrorHandlingMiddleware())   # 1st in, last out
mcp.add_middleware(RateLimitingMiddleware())    # 2nd in, 2nd out
mcp.add_middleware(LoggingMiddleware())         # 3rd in, first out
```

This ordering matters. Place error handling early so it catches exceptions from all subsequent middleware. Place logging late so it records the actual execution after other middleware has processed the request.

### [​](#server-composition) Server Composition

When using [mounted servers](/servers/composition), middleware behavior follows a clear hierarchy:

* **Parent middleware** runs for all requests, including those routed to mounted servers
* **Mounted server middleware** only runs for requests handled by that specific server

```
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware

parent = FastMCP("Parent")
parent.add_middleware(AuthMiddleware())  # Runs for ALL requests

child = FastMCP("Child")
child.add_middleware(LoggingMiddleware())  # Only runs for child's tools

parent.mount(child, namespace="child")
```

Requests to `child_tool` flow through the parent’s `AuthMiddleware` first, then through the child’s `LoggingMiddleware`.

## [​](#hooks) Hooks

Rather than processing every message identically, FastMCP provides specialized hooks at different levels of specificity. Multiple hooks fire for a single request, going from general to specific:

| Level | Hooks | Purpose |
| --- | --- | --- |
| Message | `on_message` | All MCP traffic (requests and notifications) |
| Type | `on_request`, `on_notification` | Requests expecting responses vs fire-and-forget |
| Operation | `on_call_tool`, `on_read_resource`, `on_get_prompt`, etc. | Specific MCP operations |

When a client calls a tool, the middleware chain processes `on_message` first, then `on_request`, then `on_call_tool`. This hierarchy lets you target exactly the right scope—use `on_message` for logging everything, `on_request` for authentication, and `on_call_tool` for tool-specific behavior.

### [​](#hook-signature) Hook Signature

Every hook follows the same pattern:

```
async def hook_name(self, context: MiddlewareContext, call_next) -> result_type:
    # Pre-processing
    result = await call_next(context)
    # Post-processing
    return result
```

**Parameters:**

* `context` — `MiddlewareContext` containing request information
* `call_next` — Async function to continue the middleware chain

**Returns:** The appropriate result type for the hook (varies by operation).

### [​](#middlewarecontext) MiddlewareContext

The `context` parameter provides access to request details:

| Attribute | Type | Description |
| --- | --- | --- |
| `method` | `str` | MCP method name (e.g., `"tools/call"`) |
| `source` | `str` | Origin: `"client"` or `"server"` |
| `type` | `str` | Message type: `"request"` or `"notification"` |
| `message` | `object` | The MCP message data |
| `timestamp` | `datetime` | When the request was received |
| `fastmcp_context` | `Context` | FastMCP context object (if available) |

### [​](#message-hooks) Message Hooks

#### [​](#on_message) on\_message

Called for every MCP message—both requests and notifications.

```
async def on_message(self, context: MiddlewareContext, call_next):
    result = await call_next(context)
    return result
```

Use for: Logging, metrics, or any cross-cutting concern that applies to all traffic.

#### [​](#on_request) on\_request

Called for MCP requests that expect a response.

```
async def on_request(self, context: MiddlewareContext, call_next):
    result = await call_next(context)
    return result
```

Use for: Authentication, authorization, request validation.

#### [​](#on_notification) on\_notification

Called for fire-and-forget MCP notifications.

```
async def on_notification(self, context: MiddlewareContext, call_next):
    await call_next(context)
    # Notifications don't return values
```

Use for: Event logging, async side effects.

### [​](#operation-hooks) Operation Hooks

#### [​](#on_call_tool) on\_call\_tool

Called when a tool is executed. The `context.message` contains `name` (tool name) and `arguments` (dict).

```
async def on_call_tool(self, context: MiddlewareContext, call_next):
    tool_name = context.message.name
    args = context.message.arguments
    result = await call_next(context)
    return result
```

**Returns:** Tool execution result or raises `ToolError`.

#### [​](#on_read_resource) on\_read\_resource

Called when a resource is read. The `context.message` contains `uri` (resource URI).

```
async def on_read_resource(self, context: MiddlewareContext, call_next):
    uri = context.message.uri
    result = await call_next(context)
    return result
```

**Returns:** Resource content.

#### [​](#on_get_prompt) on\_get\_prompt

Called when a prompt is retrieved. The `context.message` contains `name` (prompt name) and `arguments` (dict).

```
async def on_get_prompt(self, context: MiddlewareContext, call_next):
    prompt_name = context.message.name
    result = await call_next(context)
    return result
```

**Returns:** Prompt messages.

#### [​](#on_list_tools) on\_list\_tools

Called when listing available tools. Returns a list of FastMCP `Tool` objects before MCP conversion.

```
async def on_list_tools(self, context: MiddlewareContext, call_next):
    tools = await call_next(context)
    # Filter or modify the tool list
    return tools
```

**Returns:** `list[Tool]` — Can be filtered before returning to client.

#### [​](#on_list_resources) on\_list\_resources

Called when listing available resources. Returns FastMCP `Resource` objects.

```
async def on_list_resources(self, context: MiddlewareContext, call_next):
    resources = await call_next(context)
    return resources
```

**Returns:** `list[Resource]`

#### [​](#on_list_resource_templates) on\_list\_resource\_templates

Called when listing resource templates.

```
async def on_list_resource_templates(self, context: MiddlewareContext, call_next):
    templates = await call_next(context)
    return templates
```

**Returns:** `list[ResourceTemplate]`

#### [​](#on_list_prompts) on\_list\_prompts

Called when listing available prompts.

```
async def on_list_prompts(self, context: MiddlewareContext, call_next):
    prompts = await call_next(context)
    return prompts
```

**Returns:** `list[Prompt]`

#### [​](#on_initialize) on\_initialize

Called when a client connects and initializes the session. This hook cannot modify the initialization response.

```
from mcp import McpError
from mcp.types import ErrorData

async def on_initialize(self, context: MiddlewareContext, call_next):
    client_info = context.message.params.get("clientInfo", {})
    client_name = client_info.get("name", "unknown")

    # Reject before call_next to send error to client
    if client_name == "blocked-client":
        raise McpError(ErrorData(code=-32000, message="Client not supported"))

    await call_next(context)
    print(f"Client {client_name} initialized")
```

**Returns:** `None` — The initialization response is handled internally by the MCP protocol.

Raising `McpError` after `call_next()` will only log the error, not send it to the client. The response has already been sent. Always reject **before** `call_next()`.

### [​](#raw-handler) Raw Handler

For complete control over all messages, override `__call__` instead of individual hooks:

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class RawMiddleware(Middleware):
    async def __call__(self, context: MiddlewareContext, call_next):
        print(f"Processing: {context.method}")
        result = await call_next(context)
        print(f"Completed: {context.method}")
        return result
```

This bypasses the hook dispatch system entirely. Use when you need uniform handling regardless of message type.

### [​](#session-availability) Session Availability

The MCP session may not be available during certain phases like initialization. Check before accessing session-specific attributes:

```
async def on_request(self, context: MiddlewareContext, call_next):
    ctx = context.fastmcp_context

    if ctx.request_context:
        # MCP session available
        session_id = ctx.session_id
        request_id = ctx.request_id
    else:
        # Session not yet established (e.g., during initialization)
        # Use HTTP helpers if needed
        from fastmcp.server.dependencies import get_http_headers
        headers = get_http_headers()

    return await call_next(context)
```

For HTTP-specific data (headers, client IP) when using HTTP transports, see [HTTP Requests](/servers/context#http-requests).

## [​](#built-in-middleware) Built-in Middleware

FastMCP includes production-ready middleware for common server concerns.

### [​](#logging) Logging

```
from fastmcp.server.middleware.logging import LoggingMiddleware, StructuredLoggingMiddleware
```

`LoggingMiddleware` provides human-readable request and response logging. `StructuredLoggingMiddleware` outputs JSON-formatted logs for aggregation tools like Datadog or Splunk.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(LoggingMiddleware(
    include_payloads=True,
    max_payload_length=1000
))
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `include_payloads` | `bool` | `False` | Log request/response content |
| `max_payload_length` | `int` | `500` | Truncate payloads beyond this length |
| `logger` | `Logger` | module logger | Custom logger instance |

### [​](#timing) Timing

```
from fastmcp.server.middleware.timing import TimingMiddleware, DetailedTimingMiddleware
```

`TimingMiddleware` logs execution duration for all requests. `DetailedTimingMiddleware` provides per-operation timing with separate tracking for tools, resources, and prompts.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.timing import TimingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(TimingMiddleware())
```

### [​](#caching) Caching

```
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
```

Caches tool calls, resource reads, and list operations with TTL-based expiration.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.caching import ResponseCachingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(ResponseCachingMiddleware())
```

Each operation type can be configured independently using settings classes:

```
from fastmcp.server.middleware.caching import (
    ResponseCachingMiddleware,
    CallToolSettings,
    ListToolsSettings,
    ReadResourceSettings
)

mcp.add_middleware(ResponseCachingMiddleware(
    list_tools_settings=ListToolsSettings(ttl=30),
    call_tool_settings=CallToolSettings(included_tools=["expensive_tool"]),
    read_resource_settings=ReadResourceSettings(enabled=False)
))
```

| Settings Class | Configures |
| --- | --- |
| `ListToolsSettings` | `on_list_tools` caching |
| `CallToolSettings` | `on_call_tool` caching |
| `ListResourcesSettings` | `on_list_resources` caching |
| `ReadResourceSettings` | `on_read_resource` caching |
| `ListPromptsSettings` | `on_list_prompts` caching |
| `GetPromptSettings` | `on_get_prompt` caching |

Each settings class accepts:

* `enabled` — Enable/disable caching for this operation
* `ttl` — Time-to-live in seconds
* `included_*` / `excluded_*` — Whitelist or blacklist specific items

For persistence or distributed deployments, configure a different storage backend:

```
from pathlib import Path
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from key_value.aio.stores.filetree import (
    FileTreeStore,
    FileTreeV1KeySanitizationStrategy,
    FileTreeV1CollectionSanitizationStrategy,
)

cache_dir = Path("cache")
mcp.add_middleware(ResponseCachingMiddleware(
    cache_storage=FileTreeStore(
        data_directory=cache_dir,
        key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(cache_dir),
        collection_sanitization_strategy=FileTreeV1CollectionSanitizationStrategy(cache_dir),
    )
))
```

See [Storage Backends](/servers/storage-backends) for complete options.

Cache keys are based on the operation name and arguments only — they do not include user or session identity. If your tools return user-specific data derived from auth context (e.g., headers or session state) rather than from the request arguments, you should either disable caching for those tools or ensure user identity is part of the tool arguments.

### [​](#rate-limiting) Rate Limiting

```
from fastmcp.server.middleware.rate_limiting import (
    RateLimitingMiddleware,
    SlidingWindowRateLimitingMiddleware
)
```

`RateLimitingMiddleware` uses a token bucket algorithm allowing controlled bursts. `SlidingWindowRateLimitingMiddleware` provides precise time-window rate limiting without burst allowance.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(RateLimitingMiddleware(
    max_requests_per_second=10.0,
    burst_capacity=20
))
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `max_requests_per_second` | `float` | `10.0` | Sustained request rate |
| `burst_capacity` | `int` | `20` | Maximum burst size |
| `client_id_func` | `Callable` | `None` | Custom client identification |

For sliding window rate limiting:

```
from fastmcp.server.middleware.rate_limiting import SlidingWindowRateLimitingMiddleware

mcp.add_middleware(SlidingWindowRateLimitingMiddleware(
    max_requests=100,
    window_minutes=1
))
```

### [​](#error-handling) Error Handling

```
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware, RetryMiddleware
```

`ErrorHandlingMiddleware` provides centralized error logging and transformation. `RetryMiddleware` automatically retries with exponential backoff for transient failures.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(ErrorHandlingMiddleware(
    include_traceback=True,
    transform_errors=True,
    error_callback=my_error_callback
))
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `include_traceback` | `bool` | `False` | Include stack traces in logs |
| `transform_errors` | `bool` | `False` | Convert exceptions to MCP errors |
| `error_callback` | `Callable` | `None` | Custom callback on errors |

For automatic retries:

```
from fastmcp.server.middleware.error_handling import RetryMiddleware

mcp.add_middleware(RetryMiddleware(
    max_retries=3,
    retry_exceptions=(ConnectionError, TimeoutError)
))
```

### [​](#ping) Ping

```
from fastmcp.server.middleware import PingMiddleware
```

Keeps long-lived connections alive by sending periodic pings.

```
from fastmcp import FastMCP
from fastmcp.server.middleware import PingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(PingMiddleware(interval_ms=5000))
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `interval_ms` | `int` | `30000` | Ping interval in milliseconds |

The ping task starts on the first message and stops automatically when the session ends. Most useful for stateful HTTP connections; has no effect on stateless connections.

### [​](#response-limiting) Response Limiting

```
from fastmcp.server.middleware.response_limiting import ResponseLimitingMiddleware
```

Large tool responses can overwhelm LLM context windows or cause memory issues. You can add response-limiting middleware to enforce size constraints on tool outputs.

```
from fastmcp import FastMCP
from fastmcp.server.middleware.response_limiting import ResponseLimitingMiddleware

mcp = FastMCP("MyServer")

# Limit all tool responses to 500KB
mcp.add_middleware(ResponseLimitingMiddleware(max_size=500_000))

@mcp.tool
def search(query: str) -> str:
    # This could return a very large result
    return "x" * 1_000_000  # 1MB response

# When called, the response will be truncated to ~500KB with:
# "...\n\n[Response truncated due to size limit]"
```

When a response exceeds the limit, the middleware extracts all text content, joins it together, truncates to fit within the limit, and returns a single `TextContent` block. For non-text responses, the serialized JSON is used as the text source.

If a tool defines an `output_schema`, truncated responses will no longer conform to that schema — the client will receive a plain `TextContent` block instead of the expected structured output. Keep this in mind when setting size limits for tools with structured responses.

```
# Limit only specific tools
mcp.add_middleware(ResponseLimitingMiddleware(
    max_size=100_000,
    tools=["search", "fetch_data"],
))
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `max_size` | `int` | `1_000_000` | Maximum response size in bytes (1MB default) |
| `truncation_suffix` | `str` | `"\n\n[Response truncated due to size limit]"` | Suffix appended to truncated responses |
| `tools` | `list[str] | None` | `None` | Limit only these tools (None = all tools) |

### [​](#combining-middleware) Combining Middleware

Order matters. Place middleware that should run first (on the way in) earliest:

```
from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("Production Server")

mcp.add_middleware(ErrorHandlingMiddleware())   # Catch all errors
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_second=50))
mcp.add_middleware(TimingMiddleware())
mcp.add_middleware(LoggingMiddleware())

@mcp.tool
def my_tool(data: str) -> str:
    return f"Processed: {data}"
```

## [​](#custom-middleware) Custom Middleware

When the built-in middleware doesn’t fit your needs—custom authentication schemes, domain-specific logging, or request transformation—subclass `Middleware` and override the hooks you need.

```
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

class CustomMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        # Pre-processing
        print(f"→ {context.method}")

        result = await call_next(context)

        # Post-processing
        print(f"← {context.method}")
        return result

mcp = FastMCP("MyServer")
mcp.add_middleware(CustomMiddleware())
```

Override only the hooks relevant to your use case. Unoverridden hooks pass through automatically.

### [​](#denying-requests) Denying Requests

Raise the appropriate error type to stop processing and return an error to the client.

```
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

class AuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name

        if tool_name in ["delete_all", "admin_config"]:
            raise ToolError("Access denied: requires admin privileges")

        return await call_next(context)
```

| Operation | Error Type |
| --- | --- |
| Tool calls | `ToolError` |
| Resource reads | `ResourceError` |
| Prompt retrieval | `PromptError` |
| General requests | `McpError` |

Do not return error values or skip `call_next()` to indicate errors—raise exceptions for proper error propagation.

### [​](#modifying-requests) Modifying Requests

Change the message before passing it down the chain.

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class InputSanitizer(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        if context.message.name == "search":
            # Normalize search query
            query = context.message.arguments.get("query", "")
            context.message.arguments["query"] = query.strip().lower()

        return await call_next(context)
```

### [​](#modifying-responses) Modifying Responses

Transform results after the handler executes.

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class ResponseEnricher(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        result = await call_next(context)

        if context.message.name == "get_data" and result.structured_content:
            result.structured_content["processed_by"] = "enricher"

        return result
```

For more complex tool transformations, consider [Transforms](/servers/transforms/transforms) instead.

### [​](#filtering-lists) Filtering Lists

List operations return FastMCP objects that you can filter before they reach the client. When filtering list results, also block execution in the corresponding operation hook to maintain consistency:

```
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

class PrivateToolFilter(Middleware):
    async def on_list_tools(self, context: MiddlewareContext, call_next):
        tools = await call_next(context)
        return [tool for tool in tools if "private" not in tool.tags]

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        if context.fastmcp_context:
            tool = await context.fastmcp_context.fastmcp.get_tool(context.message.name)
            if "private" in tool.tags:
                raise ToolError("Tool not found")

        return await call_next(context)
```

### [​](#accessing-component-metadata) Accessing Component Metadata

During execution hooks, component metadata (like tags) isn’t directly available. Look up the component through the server:

```
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

class TagBasedAuth(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        if context.fastmcp_context:
            try:
                tool = await context.fastmcp_context.fastmcp.get_tool(context.message.name)

                if "requires-auth" in tool.tags:
                    # Check authentication here
                    pass

            except Exception:
                pass  # Let execution handle missing tools

        return await call_next(context)
```

The same pattern works for resources and prompts:

```
resource = await context.fastmcp_context.fastmcp.get_resource(context.message.uri)
prompt = await context.fastmcp_context.fastmcp.get_prompt(context.message.name)
```

### [​](#storing-state) Storing State

Middleware can store state that tools access later through the FastMCP context.

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class UserMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        # Extract user from headers (HTTP transport)
        from fastmcp.server.dependencies import get_http_headers
        headers = get_http_headers() or {}
        user_id = headers.get("x-user-id", "anonymous")

        # Store for tools to access
        if context.fastmcp_context:
            context.fastmcp_context.set_state("user_id", user_id)

        return await call_next(context)
```

Tools retrieve the state:

```
from fastmcp import FastMCP, Context

mcp = FastMCP("MyServer")

@mcp.tool
def get_user_data(ctx: Context) -> str:
    user_id = ctx.get_state("user_id")
    return f"Data for user: {user_id}"
```

See [Context State Management](/servers/context#state-management) for details.

### [​](#constructor-parameters) Constructor Parameters

Initialize middleware with configuration:

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class ConfigurableMiddleware(Middleware):
    def __init__(self, api_key: str, rate_limit: int = 100):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.request_counts = {}

    async def on_request(self, context: MiddlewareContext, call_next):
        # Use self.api_key, self.rate_limit, etc.
        return await call_next(context)

mcp.add_middleware(ConfigurableMiddleware(
    api_key="secret",
    rate_limit=50
))
```

### [​](#error-handling-in-custom-middleware) Error Handling in Custom Middleware

Wrap `call_next()` to handle errors from downstream middleware and handlers.

```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class ErrorLogger(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        try:
            return await call_next(context)
        except Exception as e:
            print(f"Error in {context.method}: {type(e).__name__}: {e}")
            raise  # Re-raise to let error propagate
```

Catching and not re-raising suppresses the error entirely. Usually you want to log and re-raise.

### [​](#complete-example) Complete Example

Authentication middleware checking API keys for specific tools:

```
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
from fastmcp.exceptions import ToolError

class ApiKeyAuth(Middleware):
    def __init__(self, valid_keys: set[str], protected_tools: set[str]):
        self.valid_keys = valid_keys
        self.protected_tools = protected_tools

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name

        if tool_name not in self.protected_tools:
            return await call_next(context)

        headers = get_http_headers() or {}
        api_key = headers.get("x-api-key")

        if api_key not in self.valid_keys:
            raise ToolError(f"Invalid API key for protected tool: {tool_name}")

        return await call_next(context)

mcp = FastMCP("Secure Server")
mcp.add_middleware(ApiKeyAuth(
    valid_keys={"key-1", "key-2"},
    protected_tools={"delete_user", "admin_panel"}
))

@mcp.tool
def delete_user(user_id: str) -> str:
    return f"Deleted user {user_id}"

@mcp.tool
def get_user(user_id: str) -> str:
    return f"User {user_id}"  # Not protected
```

---

## 6. Enable strict validation for this server

Tools are the core building blocks that allow your LLM to interact with external systems, execute code, and access data that isn’t in its training data. In FastMCP, tools are Python functions exposed to LLMs through the MCP protocol.
Tools in FastMCP transform regular Python functions into capabilities that LLMs can invoke during conversations. When an LLM decides to use a tool:

1. It sends a request with parameters based on the tool’s schema.
2. FastMCP validates these parameters against your function’s signature.
3. Your function executes with the validated inputs.
4. The result is returned to the LLM, which can use it in its response.

This allows LLMs to perform tasks like querying databases, calling APIs, making calculations, or accessing files—extending their capabilities beyond what’s in their training data.

## [​](#the-@tool-decorator) The `@tool` Decorator

Creating a tool is as simple as decorating a Python function with `@mcp.tool`:

```
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```

When this tool is registered, FastMCP automatically:

* Uses the function name (`add`) as the tool name.
* Uses the function’s docstring (`Adds two integer numbers...`) as the tool description.
* Generates an input schema based on the function’s parameters and type annotations.
* Handles parameter validation and error reporting.

The way you define your Python function dictates how the tool appears and behaves for the LLM client.

Functions with `*args` or `**kwargs` are not supported as tools. This restriction exists because FastMCP needs to generate a complete parameter schema for the MCP protocol, which isn’t possible with variable argument lists.

### [​](#decorator-arguments) Decorator Arguments

While FastMCP infers the name and description from your function, you can override these and add additional metadata using arguments to the `@mcp.tool` decorator:

```
@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "product-team"}  # Custom metadata
)
def search_products_implementation(query: str, category: str | None = None) -> list[dict]:
    """Internal function description (ignored if description is provided above)."""
    # Implementation...
    print(f"Searching for '{query}' in category '{category}'")
    return [{"id": 2, "name": "Another Product"}]
```

## @tool Decorator Arguments

[​](#param-name)

name

str | None

Sets the explicit tool name exposed via MCP. If not provided, uses the function name

[​](#param-description)

description

str | None

Provides the description exposed via MCP. If set, the function’s docstring is ignored for this purpose

[​](#param-tags)

tags

set[str] | None

A set of strings used to categorize the tool. These can be used by the server and, in some cases, by clients to filter or group available tools.

[​](#param-enabled)

enabled

bool

default:"True"

Deprecated in v3.0.0. Use `mcp.enable()` / `mcp.disable()` at the server level instead.

A boolean to enable or disable the tool. See [Component Visibility](#component-visibility) for the recommended approach.

[​](#param-icons)

icons

list[Icon] | None

New in version `2.13.0`Optional list of icon representations for this tool. See [Icons](/servers/icons) for detailed examples

[​](#param-annotations)

annotations

ToolAnnotations | dict | None

An optional `ToolAnnotations` object or dictionary to add additional metadata about the tool.

Show ToolAnnotations attributes

[​](#param-title)

title

str | None

A human-readable title for the tool.

[​](#param-read-only-hint)

readOnlyHint

bool | None

If true, the tool does not modify its environment.

[​](#param-destructive-hint)

destructiveHint

bool | None

If true, the tool may perform destructive updates to its environment.

[​](#param-idempotent-hint)

idempotentHint

bool | None

If true, calling the tool repeatedly with the same arguments will have no additional effect on the its environment.

[​](#param-open-world-hint)

openWorldHint

bool | None

If true, this tool may interact with an “open world” of external entities. If false, the tool’s domain of interaction is closed.

[​](#param-meta)

meta

dict[str, Any] | None

New in version `2.11.0`Optional meta information about the tool. This data is passed through to the MCP client as the `meta` field of the client-side tool object and can be used for custom metadata, versioning, or other application-specific purposes.

[​](#param-timeout)

timeout

float | None

New in version `3.0.0`Execution timeout in seconds. If the tool takes longer than this to complete, an MCP error is returned to the client. See [Timeouts](#timeouts) for details.

[​](#param-version)

version

str | int | None

New in version `3.0.0`Optional version identifier for this tool. See [Versioning](/servers/versioning) for details.

[​](#param-output-schema)

output\_schema

dict[str, Any] | None

New in version `2.10.0`Optional JSON schema for the tool’s output. When provided, the tool must return structured output matching this schema. If not provided, FastMCP automatically generates a schema from the function’s return type annotation. See [Output Schemas](#output-schemas) for details.

### [​](#using-with-methods) Using with Methods

The `@mcp.tool` decorator registers tools immediately, which doesn’t work with instance or class methods (you’d see `self` or `cls` as required parameters). For methods, use the standalone `@tool` decorator to attach metadata, then register the bound method:

```
from fastmcp import FastMCP
from fastmcp.tools import tool

class Calculator:
    def __init__(self, multiplier: int):
        self.multiplier = multiplier

    @tool()
    def multiply(self, x: int) -> int:
        """Multiply x by the instance multiplier."""
        return x * self.multiplier

calc = Calculator(multiplier=3)
mcp = FastMCP()
mcp.add_tool(calc.multiply)  # Registers with correct schema (only 'x', not 'self')
```

### [​](#async-support) Async Support

FastMCP supports both asynchronous (`async def`) and synchronous (`def`) functions as tools. Synchronous tools automatically run in a threadpool to avoid blocking the event loop, so multiple tool calls can execute concurrently even if individual tools perform blocking operations.

```
from fastmcp import FastMCP
import time

mcp = FastMCP()

@mcp.tool
def slow_tool(x: int) -> int:
    """This sync function won't block other concurrent requests."""
    time.sleep(2)  # Runs in threadpool, not on the event loop
    return x * 2
```

For I/O-bound operations like network requests or database queries, async tools are still preferred since they’re more efficient than threadpool dispatch. Use sync tools when working with synchronous libraries or for simple operations where the threading overhead doesn’t matter.

## [​](#arguments) Arguments

By default, FastMCP converts Python functions into MCP tools by inspecting the function’s signature and type annotations. This allows you to use standard Python type annotations for your tools. In general, the framework strives to “just work”: idiomatic Python behaviors like parameter defaults and type annotations are automatically translated into MCP schemas. However, there are a number of ways to customize the behavior of your tools.

FastMCP automatically dereferences `$ref` entries in tool schemas to ensure compatibility with MCP clients that don’t fully support JSON Schema references (e.g., VS Code Copilot, Claude Desktop). This means complex Pydantic models with shared types are inlined in the schema rather than using `$defs` references.Dereferencing happens at serve-time via middleware, so your schemas are stored with `$ref` intact and only inlined when sent to clients. If you know your clients handle `$ref` correctly and prefer smaller schemas, you can opt out:

```
mcp = FastMCP("my-server", dereference_schemas=False)
```

### [​](#type-annotations) Type Annotations

MCP tools have typed arguments, and FastMCP uses type annotations to determine those types. Therefore, you should use standard Python type annotations for tool arguments:

```
@mcp.tool
def analyze_text(
    text: str,
    max_tokens: int = 100,
    language: str | None = None
) -> dict:
    """Analyze the provided text."""
    # Implementation...
```

FastMCP supports a wide range of type annotations, including all Pydantic types:

| Type Annotation | Example | Description |
| --- | --- | --- |
| Basic types | `int`, `float`, `str`, `bool` | Simple scalar values |
| Binary data | `bytes` | Binary content (raw strings, not auto-decoded base64) |
| Date and Time | `datetime`, `date`, `timedelta` | Date and time objects (ISO format strings) |
| Collection types | `list[str]`, `dict[str, int]`, `set[int]` | Collections of items |
| Optional types | `float | None`, `Optional[float]` | Parameters that may be null/omitted |
| Union types | `str | int`, `Union[str, int]` | Parameters accepting multiple types |
| Constrained types | `Literal["A", "B"]`, `Enum` | Parameters with specific allowed values |
| Paths | `Path` | File system paths (auto-converted from strings) |
| UUIDs | `UUID` | Universally unique identifiers (auto-converted from strings) |
| Pydantic models | `UserData` | Complex structured data with validation |

FastMCP supports all types that Pydantic supports as fields, including all Pydantic custom types. A few FastMCP-specific behaviors to note:
**Binary Data**: `bytes` parameters accept raw strings without automatic base64 decoding. For base64 data, use `str` and decode manually with `base64.b64decode()`.
**Enums**: Clients send enum values (`"red"`), not names (`"RED"`). Your function receives the Enum member (`Color.RED`).
**Paths and UUIDs**: String inputs are automatically converted to `Path` and `UUID` objects.
**Pydantic Models**: Must be provided as JSON objects (dicts), not stringified JSON. Even with flexible validation, `{"user": {"name": "Alice"}}` works, but `{"user": '{"name": "Alice"}'}` does not.

### [​](#optional-arguments) Optional Arguments

FastMCP follows Python’s standard function parameter conventions. Parameters without default values are required, while those with default values are optional.

```
@mcp.tool
def search_products(
    query: str,                   # Required - no default value
    max_results: int = 10,        # Optional - has default value
    sort_by: str = "relevance",   # Optional - has default value
    category: str | None = None   # Optional - can be None
) -> list[dict]:
    """Search the product catalog."""
    # Implementation...
```

In this example, the LLM must provide a `query` parameter, while `max_results`, `sort_by`, and `category` will use their default values if not explicitly provided.

### [​](#validation-modes) Validation Modes

New in version `2.13.0`
By default, FastMCP uses Pydantic’s flexible validation that coerces compatible inputs to match your type annotations. This improves compatibility with LLM clients that may send string representations of values (like `"10"` for an integer parameter).
If you need stricter validation that rejects any type mismatches, you can enable strict input validation. Strict mode uses the MCP SDK’s built-in JSON Schema validation to validate inputs against the exact schema before passing them to your function:

```
# Enable strict validation for this server
mcp = FastMCP("StrictServer", strict_input_validation=True)

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# With strict_input_validation=True, sending {"a": "10", "b": "20"} will fail
# With strict_input_validation=False (default), it will be coerced to integers
```

**Validation Behavior Comparison:**

| Input Type | strict\_input\_validation=False (default) | strict\_input\_validation=True |
| --- | --- | --- |
| String integers (`"10"` for `int`) | ✅ Coerced to integer | ❌ Validation error |
| String floats (`"3.14"` for `float`) | ✅ Coerced to float | ❌ Validation error |
| String booleans (`"true"` for `bool`) | ✅ Coerced to boolean | ❌ Validation error |
| Lists with string elements (`["1", "2"]` for `list[int]`) | ✅ Elements coerced | ❌ Validation error |
| Pydantic model fields with type mismatches | ✅ Fields coerced | ❌ Validation error |
| Invalid values (`"abc"` for `int`) | ❌ Validation error | ❌ Validation error |

**Note on Pydantic Models:** Even with `strict_input_validation=False`, Pydantic model parameters must be provided as JSON objects (dicts), not as stringified JSON. For example, `{"user": {"name": "Alice"}}` works, but `{"user": '{"name": "Alice"}'}` does not.

The default flexible validation mode is recommended for most use cases as it handles common LLM client behaviors gracefully while still providing strong type safety through Pydantic’s validation.

### [​](#parameter-metadata) Parameter Metadata

You can provide additional metadata about parameters in several ways:

#### [​](#simple-string-descriptions) Simple String Descriptions

New in version `2.11.0`
For basic parameter descriptions, you can use a convenient shorthand with `Annotated`:

```
from typing import Annotated

@mcp.tool
def process_image(
    image_url: Annotated[str, "URL of the image to process"],
    resize: Annotated[bool, "Whether to resize the image"] = False,
    width: Annotated[int, "Target width in pixels"] = 800,
    format: Annotated[str, "Output image format"] = "jpeg"
) -> dict:
    """Process an image with optional resizing."""
    # Implementation...
```

This shorthand syntax is equivalent to using `Field(description=...)` but more concise for simple descriptions.

This shorthand syntax is only applied to `Annotated` types with a single string description.

#### [​](#advanced-metadata-with-field) Advanced Metadata with Field

For validation constraints and advanced metadata, use Pydantic’s `Field` class with `Annotated`:

```
from typing import Annotated
from pydantic import Field

@mcp.tool
def process_image(
    image_url: Annotated[str, Field(description="URL of the image to process")],
    resize: Annotated[bool, Field(description="Whether to resize the image")] = False,
    width: Annotated[int, Field(description="Target width in pixels", ge=1, le=2000)] = 800,
    format: Annotated[
        Literal["jpeg", "png", "webp"],
        Field(description="Output image format")
    ] = "jpeg"
) -> dict:
    """Process an image with optional resizing."""
    # Implementation...
```

You can also use the Field as a default value, though the Annotated approach is preferred:

```
@mcp.tool
def search_database(
    query: str = Field(description="Search query string"),
    limit: int = Field(10, description="Maximum number of results", ge=1, le=100)
) -> list:
    """Search the database with the provided query."""
    # Implementation...
```

Field provides several validation and documentation features:

* `description`: Human-readable explanation of the parameter (shown to LLMs)
* `ge`/`gt`/`le`/`lt`: Greater/less than (or equal) constraints
* `min_length`/`max_length`: String or collection length constraints
* `pattern`: Regex pattern for string validation
* `default`: Default value if parameter is omitted

### [​](#hiding-parameters-from-the-llm) Hiding Parameters from the LLM

New in version `2.14.0`
To inject values at runtime without exposing them to the LLM (such as `user_id`, credentials, or database connections), use dependency injection with `Depends()`. Parameters using `Depends()` are automatically excluded from the tool schema:

```
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

mcp = FastMCP()

def get_user_id() -> str:
    return "user_123"  # Injected at runtime

@mcp.tool
def get_user_details(user_id: str = Depends(get_user_id)) -> str:
    # user_id is injected by the server, not provided by the LLM
    return f"Details for {user_id}"
```

See [Custom Dependencies](/servers/context#custom-dependencies) for more details on dependency injection.

## [​](#return-values) Return Values

FastMCP tools can return data in two complementary formats: **traditional content blocks** (like text and images) and **structured outputs** (machine-readable JSON). When you add return type annotations, FastMCP automatically generates **output schemas** to validate the structured data and enables clients to deserialize results back to Python objects.
Understanding how these three concepts work together:

* **Return Values**: What your Python function returns (determines both content blocks and structured data)
* **Structured Outputs**: JSON data sent alongside traditional content for machine processing
* **Output Schemas**: JSON Schema declarations that describe and validate the structured output format

The following sections explain each concept in detail.

### [​](#content-blocks) Content Blocks

FastMCP automatically converts tool return values into appropriate MCP content blocks:

* **`str`**: Sent as `TextContent`
* **`bytes`**: Base64 encoded and sent as `BlobResourceContents` (within an `EmbeddedResource`)
* **`fastmcp.utilities.types.Image`**: Sent as `ImageContent`
* **`fastmcp.utilities.types.Audio`**: Sent as `AudioContent`
* **`fastmcp.utilities.types.File`**: Sent as base64-encoded `EmbeddedResource`
* **MCP SDK content blocks**: Sent as-is
* **A list of any of the above**: Converts each item according to the above rules
* **`None`**: Results in an empty response

#### [​](#media-helper-classes) Media Helper Classes

FastMCP provides helper classes for returning images, audio, and files. When you return one of these classes, either directly or as part of a list, FastMCP automatically converts it to the appropriate MCP content block. For example, if you return a `fastmcp.utilities.types.Image` object, FastMCP will convert it to an MCP `ImageContent` block with the correct MIME type and base64 encoding.

```
from fastmcp.utilities.types import Image, Audio, File

@mcp.tool
def get_chart() -> Image:
    """Generate a chart image."""
    return Image(path="chart.png")

@mcp.tool
def get_multiple_charts() -> list[Image]:
    """Return multiple charts."""
    return [Image(path="chart1.png"), Image(path="chart2.png")]
```

Helper classes are only automatically converted to MCP content blocks when returned **directly** or as part of a **list**. For more complex containers like dicts, you can manually convert them to MCP types:

```
# ✅ Automatic conversion
return Image(path="chart.png")
return [Image(path="chart1.png"), "text content"]

# ❌ Will not be automatically converted
return {"image": Image(path="chart.png")}

# ✅ Manual conversion for nested use
return {"image": Image(path="chart.png").to_image_content()}
```

Each helper class accepts either `path=` or `data=` (mutually exclusive):

* **`path`**: File path (string or Path object) - MIME type detected from extension
* **`data`**: Raw bytes - requires `format=` parameter for MIME type
* **`format`**: Optional format override (e.g., “png”, “wav”, “pdf”)
* **`name`**: Optional name for `File` when using `data=`
* **`annotations`**: Optional MCP annotations for the content

### [​](#structured-output) Structured Output

New in version `2.10.0`
The 6/18/2025 MCP spec update [introduced](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content) structured content, which is a new way to return data from tools. Structured content is a JSON object that is sent alongside traditional content. FastMCP automatically creates structured outputs alongside traditional content when your tool returns data that has a JSON object representation. This provides machine-readable JSON data that clients can deserialize back to Python objects.
**Automatic Structured Content Rules:**

* **Object-like results** (`dict`, Pydantic models, dataclasses) → Always become structured content (even without output schema)
* **Non-object results** (`int`, `str`, `list`) → Only become structured content if there’s an output schema to validate/serialize them
* **All results** → Always become traditional content blocks for backward compatibility

This automatic behavior enables clients to receive machine-readable data alongside human-readable content without requiring explicit output schemas for object-like returns.

#### [​](#dictionaries-and-objects) Dictionaries and Objects

When your tool returns a dictionary, dataclass, or Pydantic model, FastMCP automatically creates structured content from it. The structured content contains the actual object data, making it easy for clients to deserialize back to native objects.

```
@mcp.tool
def get_user_data(user_id: str) -> dict:
    """Get user data."""
    return {"name": "Alice", "age": 30, "active": True}
```

#### [​](#primitives-and-collections) Primitives and Collections

When your tool returns a primitive type (int, str, bool) or a collection (list, set), FastMCP needs a return type annotation to generate structured content. The annotation tells FastMCP how to validate and serialize the result.
Without a type annotation, the tool only produces `content`:

```
@mcp.tool
def calculate_sum(a: int, b: int):
    """Calculate sum without return annotation."""
    return a + b  # Returns 8
```

When you add a return annotation, such as `-> int`, FastMCP generates `structuredContent` by wrapping the primitive value in a `{"result": ...}` object, since JSON schemas require object-type roots for structured output:

```
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum with return annotation."""
    return a + b  # Returns 8
```

#### [​](#typed-models) Typed Models

Return type annotations work with any type that can be converted to a JSON schema. Dataclasses and Pydantic models are particularly useful because FastMCP extracts their field definitions to create detailed schemas.

```
from dataclasses import dataclass
from fastmcp import FastMCP

mcp = FastMCP()

@dataclass
class Person:
    name: str
    age: int
    email: str

@mcp.tool
def get_user_profile(user_id: str) -> Person:
    """Get a user's profile information."""
    return Person(
        name="Alice",
        age=30,
        email="alice@example.com",
    )
```

The `Person` dataclass becomes an output schema (second tab) that describes the expected format. When executed, clients receive the result (third tab) with both `content` and `structuredContent` fields.

### [​](#output-schemas) Output Schemas

New in version `2.10.0`
The 6/18/2025 MCP spec update [introduced](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema) output schemas, which are a new way to describe the expected output format of a tool. When an output schema is provided, the tool *must* return structured output that matches the schema.
When you add return type annotations to your functions, FastMCP automatically generates JSON schemas that describe the expected output format. These schemas help MCP clients understand and validate the structured data they receive.

#### [​](#primitive-type-wrapping) Primitive Type Wrapping

For primitive return types (like `int`, `str`, `bool`), FastMCP automatically wraps the result under a `"result"` key to create valid structured output:

```
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

#### [​](#manual-schema-control) Manual Schema Control

You can override the automatically generated schema by providing a custom `output_schema`:

```
@mcp.tool(output_schema={
    "type": "object",
    "properties": {
        "data": {"type": "string"},
        "metadata": {"type": "object"}
    }
})
def custom_schema_tool() -> dict:
    """Tool with custom output schema."""
    return {"data": "Hello", "metadata": {"version": "1.0"}}
```

Schema generation works for most common types including basic types, collections, union types, Pydantic models, TypedDict structures, and dataclasses.

**Important Constraints**:

* Output schemas must be object types (`"type": "object"`)
* If you provide an output schema, your tool **must** return structured output that matches it
* However, you can provide structured output without an output schema (using `ToolResult`)

### [​](#toolresult-and-metadata) ToolResult and Metadata

For complete control over tool responses, return a `ToolResult` object. This gives you explicit control over all aspects of the tool’s output: traditional content, structured data, and metadata.

```
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

@mcp.tool
def advanced_tool() -> ToolResult:
    """Tool with full control over output."""
    return ToolResult(
        content=[TextContent(type="text", text="Human-readable summary")],
        structured_content={"data": "value", "count": 42},
        meta={"execution_time_ms": 145}
    )
```

`ToolResult` accepts three fields:
**`content`** - The traditional MCP content blocks that clients display to users. Can be a string (automatically converted to `TextContent`), a list of MCP content blocks, or any serializable value (converted to JSON string). At least one of `content` or `structured_content` must be provided.

```
# Simple string
ToolResult(content="Hello, world!")

# List of content blocks
ToolResult(content=[
    TextContent(type="text", text="Result: 42"),
    ImageContent(type="image", data="base64...", mimeType="image/png")
])
```

**`structured_content`** - A dictionary containing structured data that matches your tool’s output schema. This enables clients to programmatically process the results. If you provide `structured_content`, it must be a dictionary or `None`. If only `structured_content` is provided, it will also be used as `content` (converted to JSON string).

```
ToolResult(
    content="Found 3 users",
    structured_content={"users": [{"name": "Alice"}, {"name": "Bob"}]}
)
```

**`meta`**
New in version `2.13.1`
Runtime metadata about the tool execution. Use this for performance metrics, debugging information, or any client-specific data that doesn’t belong in the content or structured output.

```
ToolResult(
    content="Analysis complete",
    structured_content={"result": "positive"},
    meta={
        "execution_time_ms": 145,
        "model_version": "2.1",
        "confidence": 0.95
    }
)
```

The `meta` field in `ToolResult` is for runtime metadata about tool execution (e.g., execution time, performance metrics). This is separate from the `meta` parameter in `@mcp.tool(meta={...})`, which provides static metadata about the tool definition itself.

When returning `ToolResult`, you have full control - FastMCP won’t automatically wrap or transform your data. `ToolResult` can be returned with or without an output schema.

### [​](#custom-serialization) Custom Serialization

When you need custom serialization (like YAML, Markdown tables, or specialized formats), return `ToolResult` with your serialized content. This makes the serialization explicit and visible in your tool’s code:

```
import yaml
from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult

mcp = FastMCP("MyServer")

@mcp.tool
def get_config() -> ToolResult:
    """Returns configuration as YAML."""
    data = {"api_key": "abc123", "debug": True, "rate_limit": 100}
    return ToolResult(
        content=yaml.dump(data, sort_keys=False),
        structured_content=data
    )
```

For reusable serialization across multiple tools, create a wrapper decorator that returns `ToolResult`. This lets you compose serializers with other behaviors (logging, validation, caching) and keeps the serialization visible at the tool definition. See [examples/custom\_tool\_serializer\_decorator.py](https://github.com/PrefectHQ/fastmcp/blob/main/examples/custom_tool_serializer_decorator.py) for a complete implementation.

## [​](#error-handling) Error Handling

New in version `2.4.1`
If your tool encounters an error, you can raise a standard Python exception (`ValueError`, `TypeError`, `FileNotFoundError`, custom exceptions, etc.) or a FastMCP `ToolError`.
By default, all exceptions (including their details) are logged and converted into an MCP error response to be sent back to the client LLM. This helps the LLM understand failures and react appropriately.
If you want to mask internal error details for security reasons, you can:

1. Use the `mask_error_details=True` parameter when creating your `FastMCP` instance:

```
mcp = FastMCP(name="SecureServer", mask_error_details=True)
```

2. Or use `ToolError` to explicitly control what error information is sent to clients:

```
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        # Error messages from ToolError are always sent to clients,
        # regardless of mask_error_details setting
        raise ToolError("Division by zero is not allowed.")

    # If mask_error_details=True, this message would be masked
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers.")

    return a / b
```

When `mask_error_details=True`, only error messages from `ToolError` will include details, other exceptions will be converted to a generic message.

## [​](#timeouts) Timeouts

New in version `3.0.0`
Tools can specify a `timeout` parameter to limit how long execution can take. When the timeout is exceeded, the client receives an MCP error and the tool stops processing. This protects your server from unexpectedly slow operations that could block resources or leave clients waiting indefinitely.

```
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool(timeout=30.0)
async def fetch_data(url: str) -> dict:
    """Fetch data with a 30-second timeout."""
    # If this takes longer than 30 seconds,
    # the client receives an MCP error
    ...
```

Timeouts are specified in seconds as a float. When a tool exceeds its timeout, FastMCP returns an MCP error with code `-32000` and a message indicating which tool timed out and how long it ran. Both sync and async tools support timeouts—sync functions run in thread pools, so the timeout applies to the entire operation regardless of execution model.

Tools must explicitly opt-in to timeouts. There is no server-level default timeout setting.

### [​](#timeouts-vs-background-tasks) Timeouts vs Background Tasks

Timeouts apply to **foreground execution**—when a tool runs directly in response to a client request. They protect your server from tools that unexpectedly hang due to network issues, resource contention, or other transient problems.

The `timeout` parameter does **not** apply to background tasks. When a tool runs as a background task (`task=True`), execution happens in a Docket worker where the FastMCP timeout is not enforced.For task timeouts, use Docket’s `Timeout` dependency directly in your function signature:

```
from datetime import timedelta
from docket import Timeout

@mcp.tool(task=True)
async def long_running_task(
    data: str,
    timeout: Timeout = Timeout(timedelta(minutes=10))
) -> str:
    """Task with a 10-minute timeout enforced by Docket."""
    ...
```

See the [Docket documentation](https://chrisguidry.github.io/docket/dependencies/#task-timeouts) for more on task timeouts and retries.

When a tool times out, FastMCP logs a warning suggesting task mode. For operations you know will be long-running, use `task=True` instead—background tasks offload work to distributed workers and let clients poll for progress.

## [​](#component-visibility) Component Visibility

New in version `3.0.0`
You can control which tools are enabled for clients using server-level enabled control. Disabled tools don’t appear in `list_tools` and can’t be called.

```
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool(tags={"admin"})
def admin_action() -> str:
    """Admin-only action."""
    return "Done"

@mcp.tool(tags={"public"})
def public_action() -> str:
    """Public action."""
    return "Done"

# Disable specific tools by key
mcp.disable(keys={"tool:admin_action"})

# Disable tools by tag
mcp.disable(tags={"admin"})

# Or use allowlist mode - only enable tools with specific tags
mcp.enable(tags={"public"}, only=True)
```

See [Visibility](/servers/visibility) for the complete visibility control API including key formats, tag-based filtering, and provider-level control.

## [​](#mcp-annotations) MCP Annotations

New in version `2.2.7`
FastMCP allows you to add specialized metadata to your tools through annotations. These annotations communicate how tools behave to client applications without consuming token context in LLM prompts.
Annotations serve several purposes in client applications:

* Adding user-friendly titles for display purposes
* Indicating whether tools modify data or systems
* Describing the safety profile of tools (destructive vs. non-destructive)
* Signaling if tools interact with external systems

You can add annotations to a tool using the `annotations` parameter in the `@mcp.tool` decorator:

```
@mcp.tool(
    annotations={
        "title": "Calculate Sum",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def calculate_sum(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

FastMCP supports these standard annotations:

| Annotation | Type | Default | Purpose |
| --- | --- | --- | --- |
| `title` | string | - | Display name for user interfaces |
| `readOnlyHint` | boolean | false | Indicates if the tool only reads without making changes |
| `destructiveHint` | boolean | true | For non-readonly tools, signals if changes are destructive |
| `idempotentHint` | boolean | false | Indicates if repeated identical calls have the same effect as a single call |
| `openWorldHint` | boolean | true | Specifies if the tool interacts with external systems |

Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and safety controls, but won’t enforce security boundaries on their own. Always focus on making your annotations accurately represent what your tool actually does.

### [​](#using-annotation-hints) Using Annotation Hints

MCP clients like Claude and ChatGPT use annotation hints to determine when to skip confirmation prompts and how to present tools to users. The most commonly used hint is `readOnlyHint`, which signals that a tool only reads data without making changes.
**Read-only tools** improve user experience by:

* Skipping confirmation prompts for safe operations
* Allowing broader access without security concerns
* Enabling more aggressive batching and caching

Mark a tool as read-only when it retrieves data, performs calculations, or checks status without modifying state:

```
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("Data Server")

@mcp.tool(annotations={"readOnlyHint": True})
def get_user(user_id: str) -> dict:
    """Retrieve user information by ID."""
    return {"id": user_id, "name": "Alice"}

@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        idempotentHint=True,  # Same result for repeated calls
        openWorldHint=False   # Only internal data
    )
)
def search_products(query: str) -> list[dict]:
    """Search the product catalog."""
    return [{"id": 1, "name": "Widget", "price": 29.99}]

# Write operations - no readOnlyHint
@mcp.tool()
def update_user(user_id: str, name: str) -> dict:
    """Update user information."""
    return {"id": user_id, "name": name, "updated": True}

@mcp.tool(annotations={"destructiveHint": True})
def delete_user(user_id: str) -> dict:
    """Permanently delete a user account."""
    return {"deleted": user_id}
```

For tools that write to databases, send notifications, create/update/delete resources, or trigger workflows, omit `readOnlyHint` or set it to `False`. Use `destructiveHint=True` for operations that cannot be undone.
Client-specific behavior:

* **ChatGPT**: Skips confirmation prompts for read-only tools in Chat mode (see [ChatGPT integration](/integrations/chatgpt))
* **Claude**: Uses hints to understand tool safety profiles and make better execution decisions

## [​](#notifications) Notifications

New in version `2.9.1`
FastMCP automatically sends `notifications/tools/list_changed` notifications to connected clients when tools are added, removed, enabled, or disabled. This allows clients to stay up-to-date with the current tool set without manually polling for changes.

```
@mcp.tool
def example_tool() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_tool(example_tool)              # Sends tools/list_changed notification
mcp.disable(keys={"tool:example_tool"}) # Sends tools/list_changed notification
mcp.enable(keys={"tool:example_tool"})  # Sends tools/list_changed notification
mcp.local_provider.remove_tool("example_tool")  # Sends tools/list_changed notification
```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.
Clients can handle these notifications using a [message handler](/clients/notifications) to automatically refresh their tool lists or update their interfaces.

## [​](#accessing-the-mcp-context) Accessing the MCP Context

Tools can access MCP features like logging, reading resources, or reporting progress through the `Context` object. To use it, add a parameter to your tool function with the type hint `Context`.

```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")

@mcp.tool
async def process_data(data_uri: str, ctx: Context) -> dict:
    """Process data from a resource with progress reporting."""
    await ctx.info(f"Processing data from {data_uri}")

    # Read a resource
    resource = await ctx.read_resource(data_uri)
    data = resource[0].content if resource else ""

    # Report progress
    await ctx.report_progress(progress=50, total=100)

    # Example request to the client's LLM for help
    summary = await ctx.sample(f"Summarize this in 10 words: {data[:200]}")

    await ctx.report_progress(progress=100, total=100)
    return {
        "length": len(data),
        "summary": summary.text
    }
```

The Context object provides access to:

* **Logging**: `ctx.debug()`, `ctx.info()`, `ctx.warning()`, `ctx.error()`
* **Progress Reporting**: `ctx.report_progress(progress, total)`
* **Resource Access**: `ctx.read_resource(uri)`
* **LLM Sampling**: `ctx.sample(...)`
* **Request Information**: `ctx.request_id`, `ctx.client_id`

For full documentation on the Context object and all its capabilities, see the [Context documentation](/servers/context).

## [​](#server-behavior) Server Behavior

### [​](#duplicate-tools) Duplicate Tools

New in version `2.1.0`
You can control how the FastMCP server behaves if you try to register multiple tools with the same name. This is configured using the `on_duplicate_tools` argument when creating the `FastMCP` instance.

```
from fastmcp import FastMCP

mcp = FastMCP(
    name="StrictServer",
    # Configure behavior for duplicate tool names
    on_duplicate_tools="error"
)

@mcp.tool
def my_tool(): return "Version 1"

# This will now raise a ValueError because 'my_tool' already exists
# and on_duplicate_tools is set to "error".
# @mcp.tool
# def my_tool(): return "Version 2"
```

The duplicate behavior options are:

* `"warn"` (default): Logs a warning and the new tool replaces the old one.
* `"error"`: Raises a `ValueError`, preventing the duplicate registration.
* `"replace"`: Silently replaces the existing tool with the new one.
* `"ignore"`: Keeps the original tool and ignores the new registration attempt.

### [​](#removing-tools) Removing Tools

New in version `2.3.4`
You can dynamically remove tools from a server through its [local provider](/servers/providers/local):

```
from fastmcp import FastMCP

mcp = FastMCP(name="DynamicToolServer")

@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

mcp.local_provider.remove_tool("calculate_sum")
```

## [​](#versioning) Versioning

New in version `3.0.0`
Tools support versioning, allowing you to maintain multiple implementations under the same name while clients automatically receive the highest version. See [Versioning](/servers/versioning) for complete documentation on version comparison, retrieval, and migration patterns.

---

## Bibliography

1. [Run with HTTP transport](https://gofastmcp.com/servers/server)
2. [Utility function that needs context but doesn't receive it as a parameter](https://gofastmcp.com/servers/context)
3. [Basic prompt returning a string (converted to user message automatically)](https://gofastmcp.com/servers/prompts)
4. [Basic dynamic resource returning a string](https://gofastmcp.com/servers/resources)
5. [Limit all tool responses to 500KB](https://gofastmcp.com/servers/middleware)
6. [Enable strict validation for this server](https://gofastmcp.com/servers/tools)