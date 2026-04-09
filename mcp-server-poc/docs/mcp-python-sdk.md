# MCP Python SDK

**Python implementation of the Model Context Protocol (MCP)**
[![PyPI][pypi-badge]][pypi-url]
[![MIT licensed][mit-badge]][mit-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]
[![Protocol][protocol-badge]][protocol-url]
[![Specification][spec-badge]][spec-url]

> [!NOTE]
> \*\*This README documents v1.x of the MCP Python SDK (the current stable release).\*\*
>
> For v1.x code and documentation, see the [`v1.x` branch](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).
> For the upcoming v2 documentation (pre-alpha, in development on `main`), see [`README.v2.md`](README.v2.md).
## Table of Contents
- [MCP Python SDK](#mcp-python-sdk)
- [Overview](#overview)
- [Installation](#installation)
- [Adding MCP to your python project](#adding-mcp-to-your-python-project)
- [Running the standalone MCP development tools](#running-the-standalone-mcp-development-tools)
- [Quickstart](#quickstart)
- [What is MCP?](#what-is-mcp)
- [Core Concepts](#core-concepts)
- [Server](#server)
- [Resources](#resources)
- [Tools](#tools)
- [Structured Output](#structured-output)
- [Prompts](#prompts)
- [Images](#images)
- [Context](#context)
- [Getting Context in Functions](#getting-context-in-functions)
- [Context Properties and Methods](#context-properties-and-methods)
- [Completions](#completions)
- [Elicitation](#elicitation)
- [Sampling](#sampling)
- [Logging and Notifications](#logging-and-notifications)
- [Authentication](#authentication)
- [FastMCP Properties](#fastmcp-properties)
- [Session Properties and Methods](#session-properties-and-methods)
- [Request Context Properties](#request-context-properties)
- [Running Your Server](#running-your-server)
- [Development Mode](#development-mode)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Direct Execution](#direct-execution)
- [Streamable HTTP Transport](#streamable-http-transport)
- [CORS Configuration for Browser-Based Clients](#cors-configuration-for-browser-based-clients)
- [Mounting to an Existing ASGI Server](#mounting-to-an-existing-asgi-server)
- [StreamableHTTP servers](#streamablehttp-servers)
- [Basic mounting](#basic-mounting)
- [Host-based routing](#host-based-routing)
- [Multiple servers with path configuration](#multiple-servers-with-path-configuration)
- [Path configuration at initialization](#path-configuration-at-initialization)
- [SSE servers](#sse-servers)
- [Advanced Usage](#advanced-usage)
- [Low-Level Server](#low-level-server)
- [Structured Output Support](#structured-output-support)
- [Pagination (Advanced)](#pagination-advanced)
- [Writing MCP Clients](#writing-mcp-clients)
- [Client Display Utilities](#client-display-utilities)
- [OAuth Authentication for Clients](#oauth-authentication-for-clients)
- [Parsing Tool Results](#parsing-tool-results)
- [MCP Primitives](#mcp-primitives)
- [Server Capabilities](#server-capabilities)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
[pypi-badge]: https://img.shields.io/pypi/v/mcp.svg
[pypi-url]: https://pypi.org/project/mcp/
[mit-badge]: https://img.shields.io/pypi/l/mcp.svg
[mit-url]: https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE
[python-badge]: https://img.shields.io/pypi/pyversions/mcp.svg
[python-url]: https://www.python.org/downloads/
[docs-badge]: https://img.shields.io/badge/docs-python--sdk-blue.svg
[docs-url]: https://modelcontextprotocol.github.io/python-sdk/
[protocol-badge]: https://img.shields.io/badge/protocol-modelcontextprotocol.io-blue.svg
[protocol-url]: https://modelcontextprotocol.io
[spec-badge]: https://img.shields.io/badge/spec-spec.modelcontextprotocol.io-blue.svg
[spec-url]: https://modelcontextprotocol.io/specification/latest
## Overview
The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. This Python SDK implements the full MCP specification, making it easy to:
- Build MCP clients that can connect to any MCP server
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio, SSE, and Streamable HTTP
- Handle all MCP protocol messages and lifecycle events
## Installation
### Adding MCP to your python project
We recommend using [uv](https://docs.astral.sh/uv/) to manage your Python projects.
If you haven't created a uv-managed project yet, create one:
```bash
uv init mcp-server-demo
cd mcp-server-demo
```
Then add MCP to your project dependencies:
```bash
uv add "mcp[cli]"
```
Alternatively, for projects using pip for dependencies:
```bash
pip install "mcp[cli]"
```
### Running the standalone MCP development tools
To run the mcp command with uv:
```bash
uv run mcp
```
## Quickstart
Let's create a simple MCP server that exposes a calculator tool and some data:
```python
"""
FastMCP quickstart example.
Run from the repository root:
uv run examples/snippets/servers/fastmcp\_quickstart.py
"""
from mcp.server.fastmcp import FastMCP
# Create an MCP server
mcp = FastMCP("Demo", json\_response=True)
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
"""Add two numbers"""
return a + b
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get\_greeting(name: str) -> str:
"""Get a personalized greeting"""
return f"Hello, {name}!"
# Add a prompt
@mcp.prompt()
def greet\_user(name: str, style: str = "friendly") -> str:
"""Generate a greeting prompt"""
styles = {
"friendly": "Please write a warm, friendly greeting",
"formal": "Please write a formal, professional greeting",
"casual": "Please write a casual, relaxed greeting",
}
return f"{styles.get(style, styles['friendly'])} for someone named {name}."
# Run with streamable HTTP transport
if \_\_name\_\_ == "\_\_main\_\_":
mcp.run(transport="streamable-http")
```
\_Full example: [examples/snippets/servers/fastmcp\_quickstart.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/fastmcp\_quickstart.py)\_
You can install this server in [Claude Code](https://docs.claude.com/en/docs/claude-code/mcp) and interact with it right away. First, run the server:
```bash
uv run --with mcp examples/snippets/servers/fastmcp\_quickstart.py
```
Then add it to Claude Code:
```bash
claude mcp add --transport http my-server http://localhost:8000/mcp
```
Alternatively, you can test it with the MCP Inspector. Start the server as above, then in a separate terminal:
```bash
npx -y @modelcontextprotocol/inspector
```
In the inspector UI, connect to `http://localhost:8000/mcp`.
## What is MCP?
The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:
- Expose data through \*\*Resources\*\* (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
- Provide functionality through \*\*Tools\*\* (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through \*\*Prompts\*\* (reusable templates for LLM interactions)
- And more!
## Core Concepts
### Server
The FastMCP server is your core interface to the MCP protocol. It handles connection management, protocol compliance, and message routing:
```python
"""Example showing lifespan support for startup/shutdown with strong typing."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
# Mock database class for example
class Database:
"""Mock database class for example."""
@classmethod
async def connect(cls) -> "Database":
"""Connect to database."""
return cls()
async def disconnect(self) -> None:
"""Disconnect from database."""
pass
def query(self) -> str:
"""Execute a query."""
return "Query result"
@dataclass
class AppContext:
"""Application context with typed dependencies."""
db: Database
@asynccontextmanager
async def app\_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
"""Manage application lifecycle with type-safe context."""
# Initialize on startup
db = await Database.connect()
try:
yield AppContext(db=db)
finally:
# Cleanup on shutdown
await db.disconnect()
# Pass lifespan to server
mcp = FastMCP("My App", lifespan=app\_lifespan)
# Access type-safe lifespan context in tools
@mcp.tool()
def query\_db(ctx: Context[ServerSession, AppContext]) -> str:
"""Tool that uses initialized resources."""
db = ctx.request\_context.lifespan\_context.db
return db.query()
```
\_Full example: [examples/snippets/servers/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan\_example.py)\_
### Resources
Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects:
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="Resource Example")
@mcp.resource("file://documents/{name}")
def read\_document(name: str) -> str:
"""Read a document by name."""
# This would normally read from disk
return f"Content of {name}"
@mcp.resource("config://settings")
def get\_settings() -> str:
"""Get application settings."""
return """{
"theme": "dark",
"language": "en",
"debug": false
}"""
```
\_Full example: [examples/snippets/servers/basic\_resource.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic\_resource.py)\_
### Tools
Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects:
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="Tool Example")
@mcp.tool()
def sum(a: int, b: int) -> int:
"""Add two numbers together."""
return a + b
@mcp.tool()
def get\_weather(city: str, unit: str = "celsius") -> str:
"""Get weather for a city."""
# This would normally call a weather API
return f"Weather in {city}: 22degrees{unit[0].upper()}"
```
\_Full example: [examples/snippets/servers/basic\_tool.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic\_tool.py)\_
Tools can optionally receive a Context object by including a parameter with the `Context` type annotation. This context is automatically injected by the FastMCP framework and provides access to MCP capabilities:
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
mcp = FastMCP(name="Progress Example")
@mcp.tool()
async def long\_running\_task(task\_name: str, ctx: Context[ServerSession, None], steps: int = 5) -> str:
"""Execute a task with progress updates."""
await ctx.info(f"Starting: {task\_name}")
for i in range(steps):
progress = (i + 1) / steps
await ctx.report\_progress(
progress=progress,
total=1.0,
message=f"Step {i + 1}/{steps}",
)
await ctx.debug(f"Completed step {i + 1}")
return f"Task '{task\_name}' completed"
```
\_Full example: [examples/snippets/servers/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool\_progress.py)\_
#### Structured Output
Tools will return structured results by default, if their return type
annotation is compatible. Otherwise, they will return unstructured results.
Structured output supports these return types:
- Pydantic models (BaseModel subclasses)
- TypedDicts
- Dataclasses and other classes with type hints
- `dict[str, T]` (where T is any JSON-serializable type)
- Primitive types (str, int, float, bool, bytes, None) - wrapped in `{"result": value}`
- Generic types (list, tuple, Union, Optional, etc.) - wrapped in `{"result": value}`
Classes without type hints cannot be serialized for structured output. Only
classes with properly annotated attributes will be converted to Pydantic models
for schema generation and validation.
Structured results are automatically validated against the output schema
generated from the annotation. This ensures the tool returns well-typed,
validated data that clients can easily process.
\*\*Note:\*\* For backward compatibility, unstructured results are also
returned. Unstructured results are provided for backward compatibility
with previous versions of the MCP specification, and are quirks-compatible
with previous versions of FastMCP in the current version of the SDK.
\*\*Note:\*\* In cases where a tool function's return type annotation
causes the tool to be classified as structured \_and this is undesirable\_,
the classification can be suppressed by passing `structured\_output=False`
to the `@tool` decorator.
##### Advanced: Direct CallToolResult
For full control over tool responses including the `\_meta` field (for passing data to client applications without exposing it to the model), you can return `CallToolResult` directly:
```python
"""Example showing direct CallToolResult return for advanced control."""
from typing import Annotated
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
mcp = FastMCP("CallToolResult Example")
class ValidationModel(BaseModel):
"""Model for validating structured output."""
status: str
data: dict[str, int]
@mcp.tool()
def advanced\_tool() -> CallToolResult:
"""Return CallToolResult directly for full control including \_meta field."""
return CallToolResult(
content=[TextContent(type="text", text="Response visible to the model")],
\_meta={"hidden": "data for client applications only"},
)
@mcp.tool()
def validated\_tool() -> Annotated[CallToolResult, ValidationModel]:
"""Return CallToolResult with structured output validation."""
return CallToolResult(
content=[TextContent(type="text", text="Validated response")],
structuredContent={"status": "success", "data": {"result": 42}},
\_meta={"internal": "metadata"},
)
@mcp.tool()
def empty\_result\_tool() -> CallToolResult:
"""For empty results, return CallToolResult with empty content."""
return CallToolResult(content=[])
```
\_Full example: [examples/snippets/servers/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct\_call\_tool\_result.py)\_
\*\*Important:\*\* `CallToolResult` must always be returned (no `Optional` or `Union`). For empty results, use `CallToolResult(content=[])`. For optional simple types, use `str | None` without `CallToolResult`.
```python
"""Example showing structured output with tools."""
from typing import TypedDict
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Structured Output Example")
# Using Pydantic models for rich structured data
class WeatherData(BaseModel):
"""Weather information structure."""
temperature: float = Field(description="Temperature in Celsius")
humidity: float = Field(description="Humidity percentage")
condition: str
wind\_speed: float
@mcp.tool()
def get\_weather(city: str) -> WeatherData:
"""Get weather for a city - returns structured data."""
# Simulated weather data
return WeatherData(
temperature=22.5,
humidity=45.0,
condition="sunny",
wind\_speed=5.2,
)
# Using TypedDict for simpler structures
class LocationInfo(TypedDict):
latitude: float
longitude: float
name: str
@mcp.tool()
def get\_location(address: str) -> LocationInfo:
"""Get location coordinates"""
return LocationInfo(latitude=51.5074, longitude=-0.1278, name="London, UK")
# Using dict[str, Any] for flexible schemas
@mcp.tool()
def get\_statistics(data\_type: str) -> dict[str, float]:
"""Get various statistics"""
return {"mean": 42.5, "median": 40.0, "std\_dev": 5.2}
# Ordinary classes with type hints work for structured output
class UserProfile:
name: str
age: int
email: str | None = None
def \_\_init\_\_(self, name: str, age: int, email: str | None = None):
self.name = name
self.age = age
self.email = email
@mcp.tool()
def get\_user(user\_id: str) -> UserProfile:
"""Get user profile - returns structured data"""
return UserProfile(name="Alice", age=30, email="alice@example.com")
# Classes WITHOUT type hints cannot be used for structured output
class UntypedConfig:
def \_\_init\_\_(self, setting1, setting2): # type: ignore[reportMissingParameterType]
self.setting1 = setting1
self.setting2 = setting2
@mcp.tool()
def get\_config() -> UntypedConfig:
"""This returns unstructured output - no schema generated"""
return UntypedConfig("value1", "value2")
# Lists and other types are wrapped automatically
@mcp.tool()
def list\_cities() -> list[str]:
"""Get a list of cities"""
return ["London", "Paris", "Tokyo"]
# Returns: {"result": ["London", "Paris", "Tokyo"]}
@mcp.tool()
def get\_temperature(city: str) -> float:
"""Get temperature as a simple float"""
return 22.5
# Returns: {"result": 22.5}
```
\_Full example: [examples/snippets/servers/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/structured\_output.py)\_
### Prompts
Prompts are reusable templates that help LLMs interact with your server effectively:
```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
mcp = FastMCP(name="Prompt Example")
@mcp.prompt(title="Code Review")
def review\_code(code: str) -> str:
return f"Please review this code:\n\n{code}"
@mcp.prompt(title="Debug Assistant")
def debug\_error(error: str) -> list[base.Message]:
return [
base.UserMessage("I'm seeing this error:"),
base.UserMessage(error),
base.AssistantMessage("I'll help debug that. What have you tried so far?"),
]
```
\_Full example: [examples/snippets/servers/basic\_prompt.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic\_prompt.py)\_
### Icons
MCP servers can provide icons for UI display. Icons can be added to the server implementation, tools, resources, and prompts:
```python
from mcp.server.fastmcp import FastMCP, Icon
# Create an icon from a file path or URL
icon = Icon(
src="icon.png",
mimeType="image/png",
sizes="64x64"
)
# Add icons to server
mcp = FastMCP(
"My Server",
website\_url="https://example.com",
icons=[icon]
)
# Add icons to tools, resources, and prompts
@mcp.tool(icons=[icon])
def my\_tool():
"""Tool with an icon."""
return "result"
@mcp.resource("demo://resource", icons=[icon])
def my\_resource():
"""Resource with an icon."""
return "content"
```
\_Full example: [examples/fastmcp/icons\_demo.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/fastmcp/icons\_demo.py)\_
### Images
FastMCP provides an `Image` class that automatically handles image data:
```python
"""Example showing image handling with FastMCP."""
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP, Image
mcp = FastMCP("Image Example")
@mcp.tool()
def create\_thumbnail(image\_path: str) -> Image:
"""Create a thumbnail from an image"""
img = PILImage.open(image\_path)
img.thumbnail((100, 100))
return Image(data=img.tobytes(), format="png")
```
\_Full example: [examples/snippets/servers/images.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/images.py)\_
### Context
The Context object is automatically injected into tool and resource functions that request it via type hints. It provides access to MCP capabilities like logging, progress reporting, resource reading, user interaction, and request metadata.
#### Getting Context in Functions
To use context in a tool or resource function, add a parameter with the `Context` type annotation:
```python
from mcp.server.fastmcp import Context, FastMCP
mcp = FastMCP(name="Context Example")
@mcp.tool()
async def my\_tool(x: int, ctx: Context) -> str:
"""Tool that uses context capabilities."""
# The context parameter can have any name as long as it's type-annotated
return await process\_with\_context(x, ctx)
```
#### Context Properties and Methods
The Context object provides the following capabilities:
- `ctx.request\_id` - Unique ID for the current request
- `ctx.client\_id` - Client ID if available
- `ctx.fastmcp` - Access to the FastMCP server instance (see [FastMCP Properties](#fastmcp-properties))
- `ctx.session` - Access to the underlying session for advanced communication (see [Session Properties and Methods](#session-properties-and-methods))
- `ctx.request\_context` - Access to request-specific data and lifespan resources (see [Request Context Properties](#request-context-properties))
- `await ctx.debug(message)` - Send debug log message
- `await ctx.info(message)` - Send info log message
- `await ctx.warning(message)` - Send warning log message
- `await ctx.error(message)` - Send error log message
- `await ctx.log(level, message, logger\_name=None)` - Send log with custom level
- `await ctx.report\_progress(progress, total=None, message=None)` - Report operation progress
- `await ctx.read\_resource(uri)` - Read a resource by URI
- `await ctx.elicit(message, schema)` - Request additional information from user with validation
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
mcp = FastMCP(name="Progress Example")
@mcp.tool()
async def long\_running\_task(task\_name: str, ctx: Context[ServerSession, None], steps: int = 5) -> str:
"""Execute a task with progress updates."""
await ctx.info(f"Starting: {task\_name}")
for i in range(steps):
progress = (i + 1) / steps
await ctx.report\_progress(
progress=progress,
total=1.0,
message=f"Step {i + 1}/{steps}",
)
await ctx.debug(f"Completed step {i + 1}")
return f"Task '{task\_name}' completed"
```
\_Full example: [examples/snippets/servers/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool\_progress.py)\_
### Completions
MCP supports providing completion suggestions for prompt arguments and resource template parameters. With the context parameter, servers can provide completions based on previously resolved values:
Client usage:
```python
"""
cd to the `examples/snippets` directory and run:
uv run completion-client
"""
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio\_client
from mcp.types import PromptReference, ResourceTemplateReference
# Create server parameters for stdio connection
server\_params = StdioServerParameters(
command="uv", # Using uv to run the server
args=["run", "server", "completion", "stdio"], # Server with completion support
env={"UV\_INDEX": os.environ.get("UV\_INDEX", "")},
)
async def run():
"""Run the completion client example."""
async with stdio\_client(server\_params) as (read, write):
async with ClientSession(read, write) as session:
# Initialize the connection
await session.initialize()
# List available resource templates
templates = await session.list\_resource\_templates()
print("Available resource templates:")
for template in templates.resourceTemplates:
print(f" - {template.uriTemplate}")
# List available prompts
prompts = await session.list\_prompts()
print("\nAvailable prompts:")
for prompt in prompts.prompts:
print(f" - {prompt.name}")
# Complete resource template arguments
if templates.resourceTemplates:
template = templates.resourceTemplates[0]
print(f"\nCompleting arguments for resource template: {template.uriTemplate}")
# Complete without context
result = await session.complete(
ref=ResourceTemplateReference(type="ref/resource", uri=template.uriTemplate),
argument={"name": "owner", "value": "model"},
)
print(f"Completions for 'owner' starting with 'model': {result.completion.values}")
# Complete with context - repo suggestions based on owner
result = await session.complete(
ref=ResourceTemplateReference(type="ref/resource", uri=template.uriTemplate),
argument={"name": "repo", "value": ""},
context\_arguments={"owner": "modelcontextprotocol"},
)
print(f"Completions for 'repo' with owner='modelcontextprotocol': {result.completion.values}")
# Complete prompt arguments
if prompts.prompts:
prompt\_name = prompts.prompts[0].name
print(f"\nCompleting arguments for prompt: {prompt\_name}")
result = await session.complete(
ref=PromptReference(type="ref/prompt", name=prompt\_name),
argument={"name": "style", "value": ""},
)
print(f"Completions for 'style' argument: {result.completion.values}")
def main():
"""Entry point for the completion client."""
asyncio.run(run())
if \_\_name\_\_ == "\_\_main\_\_":
main()
```
\_Full example: [examples/snippets/clients/completion\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/completion\_client.py)\_
### Elicitation
Request additional information from users. This example shows an Elicitation during a Tool Call:
```python
"""Elicitation examples demonstrating form and URL mode elicitation.
Form mode elicitation collects structured, non-sensitive data through a schema.
URL mode elicitation directs users to external URLs for sensitive operations
like OAuth flows, credential collection, or payment processing.
"""
import uuid
from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.shared.exceptions import UrlElicitationRequiredError
from mcp.types import ElicitRequestURLParams
mcp = FastMCP(name="Elicitation Example")
class BookingPreferences(BaseModel):
"""Schema for collecting user preferences."""
checkAlternative: bool = Field(description="Would you like to check another date?")
alternativeDate: str = Field(
default="2024-12-26",
description="Alternative date (YYYY-MM-DD)",
)
@mcp.tool()
async def book\_table(date: str, time: str, party\_size: int, ctx: Context[ServerSession, None]) -> str:
"""Book a table with date availability check.
This demonstrates form mode elicitation for collecting non-sensitive user input.
"""
# Check if date is available
if date == "2024-12-25":
# Date unavailable - ask user for alternative
result = await ctx.elicit(
message=(f"No tables available for {party\_size} on {date}. Would you like to try another date?"),
schema=BookingPreferences,
)
if result.action == "accept" and result.data:
if result.data.checkAlternative:
return f"[SUCCESS] Booked for {result.data.alternativeDate}"
return "[CANCELLED] No booking made"
return "[CANCELLED] Booking cancelled"
# Date available
return f"[SUCCESS] Booked for {date} at {time}"
@mcp.tool()
async def secure\_payment(amount: float, ctx: Context[ServerSession, None]) -> str:
"""Process a secure payment requiring URL confirmation.
This demonstrates URL mode elicitation using ctx.elicit\_url() for
operations that require out-of-band user interaction.
"""
elicitation\_id = str(uuid.uuid4())
result = await ctx.elicit\_url(
message=f"Please confirm payment of ${amount:.2f}",
url=f"https://payments.example.com/confirm?amount={amount}&id={elicitation\_id}",
elicitation\_id=elicitation\_id,
)
if result.action == "accept":
# In a real app, the payment confirmation would happen out-of-band
# and you'd verify the payment status from your backend
return f"Payment of ${amount:.2f} initiated - check your browser to complete"
elif result.action == "decline":
return "Payment declined by user"
return "Payment cancelled"
@mcp.tool()
async def connect\_service(service\_name: str, ctx: Context[ServerSession, None]) -> str:
"""Connect to a third-party service requiring OAuth authorization.
This demonstrates the "throw error" pattern using UrlElicitationRequiredError.
Use this pattern when the tool cannot proceed without user authorization.
"""
elicitation\_id = str(uuid.uuid4())
# Raise UrlElicitationRequiredError to signal that the client must complete
# a URL elicitation before this request can be processed.
# The MCP framework will convert this to a -32042 error response.
raise UrlElicitationRequiredError(
[
ElicitRequestURLParams(
mode="url",
message=f"Authorization required to connect to {service\_name}",
url=f"https://{service\_name}.example.com/oauth/authorize?elicit={elicitation\_id}",
elicitationId=elicitation\_id,
)
]
)
```
\_Full example: [examples/snippets/servers/elicitation.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/elicitation.py)\_
Elicitation schemas support default values for all field types. Default values are automatically included in the JSON schema sent to clients, allowing them to pre-populate forms.
The `elicit()` method returns an `ElicitationResult` with:
- `action`: "accept", "decline", or "cancel"
- `data`: The validated response (only when accepted)
- `validation\_error`: Any validation error message
### Sampling
Tools can interact with LLMs through sampling (generating text):
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent
mcp = FastMCP(name="Sampling Example")
@mcp.tool()
async def generate\_poem(topic: str, ctx: Context[ServerSession, None]) -> str:
"""Generate a poem using LLM sampling."""
prompt = f"Write a short poem about {topic}"
result = await ctx.session.create\_message(
messages=[
SamplingMessage(
role="user",
content=TextContent(type="text", text=prompt),
)
],
max\_tokens=100,
)
# Since we're not passing tools param, result.content is single content
if result.content.type == "text":
return result.content.text
return str(result.content)
```
\_Full example: [examples/snippets/servers/sampling.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/sampling.py)\_
### Logging and Notifications
Tools can send logs and notifications through the context:
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
mcp = FastMCP(name="Notifications Example")
@mcp.tool()
async def process\_data(data: str, ctx: Context[ServerSession, None]) -> str:
"""Process data with logging."""
# Different log levels
await ctx.debug(f"Debug: Processing '{data}'")
await ctx.info("Info: Starting processing")
await ctx.warning("Warning: This is experimental")
await ctx.error("Error: (This is just a demo)")
# Notify about resource changes
await ctx.session.send\_resource\_list\_changed()
return f"Processed: {data}"
```
\_Full example: [examples/snippets/servers/notifications.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/notifications.py)\_
### Authentication
Authentication can be used by servers that want to expose tools accessing protected resources.
`mcp.server.auth` implements OAuth 2.1 resource server functionality, where MCP servers act as Resource Servers (RS) that validate tokens issued by separate Authorization Servers (AS). This follows the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) and implements RFC 9728 (Protected Resource Metadata) for AS discovery.
MCP servers can use authentication by providing an implementation of the `TokenVerifier` protocol:
```python
"""
Run from the repository root:
uv run examples/snippets/servers/oauth\_server.py
"""
from pydantic import AnyHttpUrl
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
class SimpleTokenVerifier(TokenVerifier):
"""Simple token verifier for demonstration."""
async def verify\_token(self, token: str) -> AccessToken | None:
pass # This is where you would implement actual token validation
# Create FastMCP instance as a Resource Server
mcp = FastMCP(
"Weather Service",
json\_response=True,
# Token verifier for authentication
token\_verifier=SimpleTokenVerifier(),
# Auth settings for RFC 9728 Protected Resource Metadata
auth=AuthSettings(
issuer\_url=AnyHttpUrl("https://auth.example.com"), # Authorization Server URL
resource\_server\_url=AnyHttpUrl("http://localhost:3001"), # This server's URL
required\_scopes=["user"],
),
)
@mcp.tool()
async def get\_weather(city: str = "London") -> dict[str, str]:
"""Get weather data for a city"""
return {
"city": city,
"temperature": "22",
"condition": "Partly cloudy",
"humidity": "65%",
}
if \_\_name\_\_ == "\_\_main\_\_":
mcp.run(transport="streamable-http")
```
\_Full example: [examples/snippets/servers/oauth\_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/oauth\_server.py)\_
For a complete example with separate Authorization Server and Resource Server implementations, see [`examples/servers/simple-auth/`](examples/servers/simple-auth/).
\*\*Architecture:\*\*
- \*\*Authorization Server (AS)\*\*: Handles OAuth flows, user authentication, and token issuance
- \*\*Resource Server (RS)\*\*: Your MCP server that validates tokens and serves protected resources
- \*\*Client\*\*: Discovers AS through RFC 9728, obtains tokens, and uses them with the MCP server
See [TokenVerifier](src/mcp/server/auth/provider.py) for more details on implementing token validation.
### FastMCP Properties
The FastMCP server instance accessible via `ctx.fastmcp` provides access to server configuration and metadata:
- `ctx.fastmcp.name` - The server's name as defined during initialization
- `ctx.fastmcp.instructions` - Server instructions/description provided to clients
- `ctx.fastmcp.website\_url` - Optional website URL for the server
- `ctx.fastmcp.icons` - Optional list of icons for UI display
- `ctx.fastmcp.settings` - Complete server configuration object containing:
- `debug` - Debug mode flag
- `log\_level` - Current logging level
- `host` and `port` - Server network configuration
- `mount\_path`, `sse\_path`, `streamable\_http\_path` - Transport paths
- `stateless\_http` - Whether the server operates in stateless mode
- And other configuration options
```python
@mcp.tool()
def server\_info(ctx: Context) -> dict:
"""Get information about the current server."""
return {
"name": ctx.fastmcp.name,
"instructions": ctx.fastmcp.instructions,
"debug\_mode": ctx.fastmcp.settings.debug,
"log\_level": ctx.fastmcp.settings.log\_level,
"host": ctx.fastmcp.settings.host,
"port": ctx.fastmcp.settings.port,
}
```
### Session Properties and Methods
The session object accessible via `ctx.session` provides advanced control over client communication:
- `ctx.session.client\_params` - Client initialization parameters and declared capabilities
- `await ctx.session.send\_log\_message(level, data, logger)` - Send log messages with full control
- `await ctx.session.create\_message(messages, max\_tokens)` - Request LLM sampling/completion
- `await ctx.session.send\_progress\_notification(token, progress, total, message)` - Direct progress updates
- `await ctx.session.send\_resource\_updated(uri)` - Notify clients that a specific resource changed
- `await ctx.session.send\_resource\_list\_changed()` - Notify clients that the resource list changed
- `await ctx.session.send\_tool\_list\_changed()` - Notify clients that the tool list changed
- `await ctx.session.send\_prompt\_list\_changed()` - Notify clients that the prompt list changed
```python
@mcp.tool()
async def notify\_data\_update(resource\_uri: str, ctx: Context) -> str:
"""Update data and notify clients of the change."""
# Perform data update logic here
# Notify clients that this specific resource changed
await ctx.session.send\_resource\_updated(AnyUrl(resource\_uri))
# If this affects the overall resource list, notify about that too
await ctx.session.send\_resource\_list\_changed()
return f"Updated {resource\_uri} and notified clients"
```
### Request Context Properties
The request context accessible via `ctx.request\_context` contains request-specific information and resources:
- `ctx.request\_context.lifespan\_context` - Access to resources initialized during server startup
- Database connections, configuration objects, shared services
- Type-safe access to resources defined in your server's lifespan function
- `ctx.request\_context.meta` - Request metadata from the client including:
- `progressToken` - Token for progress notifications
- Other client-provided metadata
- `ctx.request\_context.request` - The original MCP request object for advanced processing
- `ctx.request\_context.request\_id` - Unique identifier for this request
```python
# Example with typed lifespan context
@dataclass
class AppContext:
db: Database
config: AppConfig
@mcp.tool()
def query\_with\_config(query: str, ctx: Context) -> str:
"""Execute a query using shared database and configuration."""
# Access typed lifespan context
app\_ctx: AppContext = ctx.request\_context.lifespan\_context
# Use shared resources
connection = app\_ctx.db
settings = app\_ctx.config
# Execute query with configuration
result = connection.execute(query, timeout=settings.query\_timeout)
return str(result)
```
\_Full lifespan example: [examples/snippets/servers/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan\_example.py)\_
## Running Your Server
### Development Mode
The fastest way to test and debug your server is with the MCP Inspector:
```bash
uv run mcp dev server.py
# Add dependencies
uv run mcp dev server.py --with pandas --with numpy
# Mount local code
uv run mcp dev server.py --with-editable .
```
### Claude Desktop Integration
Once your server is ready, install it in Claude Desktop:
```bash
uv run mcp install server.py
# Custom name
uv run mcp install server.py --name "My Analytics Server"
# Environment variables
uv run mcp install server.py -v API\_KEY=abc123 -v DB\_URL=postgres://...
uv run mcp install server.py -f .env
```
### Direct Execution
For advanced scenarios like custom deployments:
```python
"""Example showing direct execution of an MCP server.
This is the simplest way to run an MCP server directly.
cd to the `examples/snippets` directory and run:
uv run direct-execution-server
or
python servers/direct\_execution.py
"""
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("My App")
@mcp.tool()
def hello(name: str = "World") -> str:
"""Say hello to someone."""
return f"Hello, {name}!"
def main():
"""Entry point for the direct execution server."""
mcp.run()
if \_\_name\_\_ == "\_\_main\_\_":
main()
```
\_Full example: [examples/snippets/servers/direct\_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct\_execution.py)\_
Run it with:
```bash
python servers/direct\_execution.py
# or
uv run mcp run servers/direct\_execution.py
```
Note that `uv run mcp run` or `uv run mcp dev` only supports server using FastMCP and not the low-level server variant.
### Streamable HTTP Transport
> \*\*Note\*\*: Streamable HTTP transport is the recommended transport for production deployments. Use `stateless\_http=True` and `json\_response=True` for optimal scalability.
```python
"""
Run from the repository root:
uv run examples/snippets/servers/streamable\_config.py
"""
from mcp.server.fastmcp import FastMCP
# Stateless server with JSON responses (recommended)
mcp = FastMCP("StatelessServer", stateless\_http=True, json\_response=True)
# Other configuration options:
# Stateless server with SSE streaming responses
# mcp = FastMCP("StatelessServer", stateless\_http=True)
# Stateful server with session persistence
# mcp = FastMCP("StatefulServer")
# Add a simple tool to demonstrate the server
@mcp.tool()
def greet(name: str = "World") -> str:
"""Greet someone by name."""
return f"Hello, {name}!"
# Run server with streamable\_http transport
if \_\_name\_\_ == "\_\_main\_\_":
mcp.run(transport="streamable-http")
```
\_Full example: [examples/snippets/servers/streamable\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_config.py)\_
You can mount multiple FastMCP servers in a Starlette application:
```python
"""
Run from the repository root:
uvicorn examples.snippets.servers.streamable\_starlette\_mount:app --reload
"""
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
# Create the Echo server
echo\_mcp = FastMCP(name="EchoServer", stateless\_http=True, json\_response=True)
@echo\_mcp.tool()
def echo(message: str) -> str:
"""A simple echo tool"""
return f"Echo: {message}"
# Create the Math server
math\_mcp = FastMCP(name="MathServer", stateless\_http=True, json\_response=True)
@math\_mcp.tool()
def add\_two(n: int) -> int:
"""Tool to add two to the input"""
return n + 2
# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
async with contextlib.AsyncExitStack() as stack:
await stack.enter\_async\_context(echo\_mcp.session\_manager.run())
await stack.enter\_async\_context(math\_mcp.session\_manager.run())
yield
# Create the Starlette app and mount the MCP servers
app = Starlette(
routes=[
Mount("/echo", echo\_mcp.streamable\_http\_app()),
Mount("/math", math\_mcp.streamable\_http\_app()),
],
lifespan=lifespan,
)
# Note: Clients connect to http://localhost:8000/echo/mcp and http://localhost:8000/math/mcp
# To mount at the root of each path (e.g., /echo instead of /echo/mcp):
# echo\_mcp.settings.streamable\_http\_path = "/"
# math\_mcp.settings.streamable\_http\_path = "/"
```
\_Full example: [examples/snippets/servers/streamable\_starlette\_mount.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_starlette\_mount.py)\_
For low level server with Streamable HTTP implementations, see:
- Stateful server: [`examples/servers/simple-streamablehttp/`](examples/servers/simple-streamablehttp/)
- Stateless server: [`examples/servers/simple-streamablehttp-stateless/`](examples/servers/simple-streamablehttp-stateless/)
The streamable HTTP transport supports:
- Stateful and stateless operation modes
- Resumability with event stores
- JSON or SSE response formats
- Better scalability for multi-node deployments
#### CORS Configuration for Browser-Based Clients
If you'd like your server to be accessible by browser-based MCP clients, you'll need to configure CORS headers. The `Mcp-Session-Id` header must be exposed for browser clients to access it:
```python
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
# Create your Starlette app first
starlette\_app = Starlette(routes=[...])
# Then wrap it with CORS middleware
starlette\_app = CORSMiddleware(
starlette\_app,
allow\_origins=["\*"], # Configure appropriately for production
allow\_methods=["GET", "POST", "DELETE"], # MCP streamable HTTP methods
expose\_headers=["Mcp-Session-Id"],
)
```
This configuration is necessary because:
- The MCP streamable HTTP transport uses the `Mcp-Session-Id` header for session management
- Browsers restrict access to response headers unless explicitly exposed via CORS
- Without this configuration, browser-based clients won't be able to read the session ID from initialization responses
### Mounting to an Existing ASGI Server
By default, SSE servers are mounted at `/sse` and Streamable HTTP servers are mounted at `/mcp`. You can customize these paths using the methods described below.
For more information on mounting applications in Starlette, see the [Starlette documentation](https://www.starlette.io/routing/#submounting-routes).
#### StreamableHTTP servers
You can mount the StreamableHTTP server to an existing ASGI server using the `streamable\_http\_app` method. This allows you to integrate the StreamableHTTP server with other ASGI applications.
##### Basic mounting
```python
"""
Basic example showing how to mount StreamableHTTP server in Starlette.
Run from the repository root:
uvicorn examples.snippets.servers.streamable\_http\_basic\_mounting:app --reload
"""
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
# Create MCP server
mcp = FastMCP("My App", json\_response=True)
@mcp.tool()
def hello() -> str:
"""A simple hello tool"""
return "Hello from MCP!"
# Create a lifespan context manager to run the session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
async with mcp.session\_manager.run():
yield
# Mount the StreamableHTTP server to the existing ASGI server
app = Starlette(
routes=[
Mount("/", app=mcp.streamable\_http\_app()),
],
lifespan=lifespan,
)
```
\_Full example: [examples/snippets/servers/streamable\_http\_basic\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_http\_basic\_mounting.py)\_
##### Host-based routing
```python
"""
Example showing how to mount StreamableHTTP server using Host-based routing.
Run from the repository root:
uvicorn examples.snippets.servers.streamable\_http\_host\_mounting:app --reload
"""
import contextlib
from starlette.applications import Starlette
from starlette.routing import Host
from mcp.server.fastmcp import FastMCP
# Create MCP server
mcp = FastMCP("MCP Host App", json\_response=True)
@mcp.tool()
def domain\_info() -> str:
"""Get domain-specific information"""
return "This is served from mcp.acme.corp"
# Create a lifespan context manager to run the session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
async with mcp.session\_manager.run():
yield
# Mount using Host-based routing
app = Starlette(
routes=[
Host("mcp.acme.corp", app=mcp.streamable\_http\_app()),
],
lifespan=lifespan,
)
```
\_Full example: [examples/snippets/servers/streamable\_http\_host\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_http\_host\_mounting.py)\_
##### Multiple servers with path configuration
```python
"""
Example showing how to mount multiple StreamableHTTP servers with path configuration.
Run from the repository root:
uvicorn examples.snippets.servers.streamable\_http\_multiple\_servers:app --reload
"""
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
# Create multiple MCP servers
api\_mcp = FastMCP("API Server", json\_response=True)
chat\_mcp = FastMCP("Chat Server", json\_response=True)
@api\_mcp.tool()
def api\_status() -> str:
"""Get API status"""
return "API is running"
@chat\_mcp.tool()
def send\_message(message: str) -> str:
"""Send a chat message"""
return f"Message sent: {message}"
# Configure servers to mount at the root of each path
# This means endpoints will be at /api and /chat instead of /api/mcp and /chat/mcp
api\_mcp.settings.streamable\_http\_path = "/"
chat\_mcp.settings.streamable\_http\_path = "/"
# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
async with contextlib.AsyncExitStack() as stack:
await stack.enter\_async\_context(api\_mcp.session\_manager.run())
await stack.enter\_async\_context(chat\_mcp.session\_manager.run())
yield
# Mount the servers
app = Starlette(
routes=[
Mount("/api", app=api\_mcp.streamable\_http\_app()),
Mount("/chat", app=chat\_mcp.streamable\_http\_app()),
],
lifespan=lifespan,
)
```
\_Full example: [examples/snippets/servers/streamable\_http\_multiple\_servers.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_http\_multiple\_servers.py)\_
##### Path configuration at initialization
```python
"""
Example showing path configuration during FastMCP initialization.
Run from the repository root:
uvicorn examples.snippets.servers.streamable\_http\_path\_config:app --reload
"""
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
# Configure streamable\_http\_path during initialization
# This server will mount at the root of wherever it's mounted
mcp\_at\_root = FastMCP(
"My Server",
json\_response=True,
streamable\_http\_path="/",
)
@mcp\_at\_root.tool()
def process\_data(data: str) -> str:
"""Process some data"""
return f"Processed: {data}"
# Mount at /process - endpoints will be at /process instead of /process/mcp
app = Starlette(
routes=[
Mount("/process", app=mcp\_at\_root.streamable\_http\_app()),
]
)
```
\_Full example: [examples/snippets/servers/streamable\_http\_path\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable\_http\_path\_config.py)\_
#### SSE servers
> \*\*Note\*\*: SSE transport is being superseded by [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).
You can mount the SSE server to an existing ASGI server using the `sse\_app` method. This allows you to integrate the SSE server with other ASGI applications.
```python
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("My App")
# Mount the SSE server to the existing ASGI server
app = Starlette(
routes=[
Mount('/', app=mcp.sse\_app()),
]
)
# or dynamically mount as host
app.router.routes.append(Host('mcp.acme.corp', app=mcp.sse\_app()))
```
When mounting multiple MCP servers under different paths, you can configure the mount path in several ways:
```python
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
# Create multiple MCP servers
github\_mcp = FastMCP("GitHub API")
browser\_mcp = FastMCP("Browser")
curl\_mcp = FastMCP("Curl")
search\_mcp = FastMCP("Search")
# Method 1: Configure mount paths via settings (recommended for persistent configuration)
github\_mcp.settings.mount\_path = "/github"
browser\_mcp.settings.mount\_path = "/browser"
# Method 2: Pass mount path directly to sse\_app (preferred for ad-hoc mounting)
# This approach doesn't modify the server's settings permanently
# Create Starlette app with multiple mounted servers
app = Starlette(
routes=[
# Using settings-based configuration
Mount("/github", app=github\_mcp.sse\_app()),
Mount("/browser", app=browser\_mcp.sse\_app()),
# Using direct mount path parameter
Mount("/curl", app=curl\_mcp.sse\_app("/curl")),
Mount("/search", app=search\_mcp.sse\_app("/search")),
]
)
# Method 3: For direct execution, you can also pass the mount path to run()
if \_\_name\_\_ == "\_\_main\_\_":
search\_mcp.run(transport="sse", mount\_path="/search")
```
For more information on mounting applications in Starlette, see the [Starlette documentation](https://www.starlette.io/routing/#submounting-routes).
## Advanced Usage
### Low-Level Server
For more control, you can use the low-level server implementation directly. This gives you full access to the protocol and allows you to customize every aspect of your server, including lifecycle management through the lifespan API:
```python
"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/lifespan.py
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
# Mock database class for example
class Database:
"""Mock database class for example."""
@classmethod
async def connect(cls) -> "Database":
"""Connect to database."""
print("Database connected")
return cls()
async def disconnect(self) -> None:
"""Disconnect from database."""
print("Database disconnected")
async def query(self, query\_str: str) -> list[dict[str, str]]:
"""Execute a query."""
# Simulate database query
return [{"id": "1", "name": "Example", "query": query\_str}]
@asynccontextmanager
async def server\_lifespan(\_server: Server) -> AsyncIterator[dict[str, Any]]:
"""Manage server startup and shutdown lifecycle."""
# Initialize resources on startup
db = await Database.connect()
try:
yield {"db": db}
finally:
# Clean up on shutdown
await db.disconnect()
# Pass lifespan to server
server = Server("example-server", lifespan=server\_lifespan)
@server.list\_tools()
async def handle\_list\_tools() -> list[types.Tool]:
"""List available tools."""
return [
types.Tool(
name="query\_db",
description="Query the database",
inputSchema={
"type": "object",
"properties": {"query": {"type": "string", "description": "SQL query to execute"}},
"required": ["query"],
},
)
]
@server.call\_tool()
async def query\_db(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
"""Handle database query tool call."""
if name != "query\_db":
raise ValueError(f"Unknown tool: {name}")
# Access lifespan context
ctx = server.request\_context
db = ctx.lifespan\_context["db"]
# Execute query
results = await db.query(arguments["query"])
return [types.TextContent(type="text", text=f"Query results: {results}")]
async def run():
"""Run the server with lifespan management."""
async with mcp.server.stdio.stdio\_server() as (read\_stream, write\_stream):
await server.run(
read\_stream,
write\_stream,
InitializationOptions(
server\_name="example-server",
server\_version="0.1.0",
capabilities=server.get\_capabilities(
notification\_options=NotificationOptions(),
experimental\_capabilities={},
),
),
)
if \_\_name\_\_ == "\_\_main\_\_":
import asyncio
asyncio.run(run())
```
\_Full example: [examples/snippets/servers/lowlevel/lifespan.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/lifespan.py)\_
The lifespan API provides:
- A way to initialize resources when the server starts and clean them up when it stops
- Access to initialized resources through the request context in handlers
- Type-safe context passing between lifespan and request handlers
```python
"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/basic.py
"""
import asyncio
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
# Create a server instance
server = Server("example-server")
@server.list\_prompts()
async def handle\_list\_prompts() -> list[types.Prompt]:
"""List available prompts."""
return [
types.Prompt(
name="example-prompt",
description="An example prompt template",
arguments=[types.PromptArgument(name="arg1", description="Example argument", required=True)],
)
]
@server.get\_prompt()
async def handle\_get\_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
"""Get a specific prompt by name."""
if name != "example-prompt":
raise ValueError(f"Unknown prompt: {name}")
arg1\_value = (arguments or {}).get("arg1", "default")
return types.GetPromptResult(
description="Example prompt",
messages=[
types.PromptMessage(
role="user",
content=types.TextContent(type="text", text=f"Example prompt text with argument: {arg1\_value}"),
)
],
)
async def run():
"""Run the basic low-level server."""
async with mcp.server.stdio.stdio\_server() as (read\_stream, write\_stream):
await server.run(
read\_stream,
write\_stream,
InitializationOptions(
server\_name="example",
server\_version="0.1.0",
capabilities=server.get\_capabilities(
notification\_options=NotificationOptions(),
experimental\_capabilities={},
),
),
)
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(run())
```
\_Full example: [examples/snippets/servers/lowlevel/basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/basic.py)\_
Caution: The `uv run mcp run` and `uv run mcp dev` tool doesn't support low-level server.
#### Structured Output Support
The low-level server supports structured output for tools, allowing you to return both human-readable content and machine-readable structured data. Tools can define an `outputSchema` to validate their structured output:
```python
"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/structured\_output.py
"""
import asyncio
from typing import Any
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
server = Server("example-server")
@server.list\_tools()
async def list\_tools() -> list[types.Tool]:
"""List available tools with structured output schemas."""
return [
types.Tool(
name="get\_weather",
description="Get current weather for a city",
inputSchema={
"type": "object",
"properties": {"city": {"type": "string", "description": "City name"}},
"required": ["city"],
},
outputSchema={
"type": "object",
"properties": {
"temperature": {"type": "number", "description": "Temperature in Celsius"},
"condition": {"type": "string", "description": "Weather condition"},
"humidity": {"type": "number", "description": "Humidity percentage"},
"city": {"type": "string", "description": "City name"},
},
"required": ["temperature", "condition", "humidity", "city"],
},
)
]
@server.call\_tool()
async def call\_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
"""Handle tool calls with structured output."""
if name == "get\_weather":
city = arguments["city"]
# Simulated weather data - in production, call a weather API
weather\_data = {
"temperature": 22.5,
"condition": "partly cloudy",
"humidity": 65,
"city": city, # Include the requested city
}
# low-level server will validate structured output against the tool's
# output schema, and additionally serialize it into a TextContent block
# for backwards compatibility with pre-2025-06-18 clients.
return weather\_data
else:
raise ValueError(f"Unknown tool: {name}")
async def run():
"""Run the structured output server."""
async with mcp.server.stdio.stdio\_server() as (read\_stream, write\_stream):
await server.run(
read\_stream,
write\_stream,
InitializationOptions(
server\_name="structured-output-example",
server\_version="0.1.0",
capabilities=server.get\_capabilities(
notification\_options=NotificationOptions(),
experimental\_capabilities={},
),
),
)
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(run())
```
\_Full example: [examples/snippets/servers/lowlevel/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/structured\_output.py)\_
Tools can return data in four ways:
1. \*\*Content only\*\*: Return a list of content blocks (default behavior before spec revision 2025-06-18)
2. \*\*Structured data only\*\*: Return a dictionary that will be serialized to JSON (Introduced in spec revision 2025-06-18)
3. \*\*Both\*\*: Return a tuple of (content, structured\_data) preferred option to use for backwards compatibility
4. \*\*Direct CallToolResult\*\*: Return `CallToolResult` directly for full control (including `\_meta` field)
When an `outputSchema` is defined, the server automatically validates the structured output against the schema. This ensures type safety and helps catch errors early.
##### Returning CallToolResult Directly
For full control over the response including the `\_meta` field (for passing data to client applications without exposing it to the model), return `CallToolResult` directly:
```python
"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/direct\_call\_tool\_result.py
"""
import asyncio
from typing import Any
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
server = Server("example-server")
@server.list\_tools()
async def list\_tools() -> list[types.Tool]:
"""List available tools."""
return [
types.Tool(
name="advanced\_tool",
description="Tool with full control including \_meta field",
inputSchema={
"type": "object",
"properties": {"message": {"type": "string"}},
"required": ["message"],
},
)
]
@server.call\_tool()
async def handle\_call\_tool(name: str, arguments: dict[str, Any]) -> types.CallToolResult:
"""Handle tool calls by returning CallToolResult directly."""
if name == "advanced\_tool":
message = str(arguments.get("message", ""))
return types.CallToolResult(
content=[types.TextContent(type="text", text=f"Processed: {message}")],
structuredContent={"result": "success", "message": message},
\_meta={"hidden": "data for client applications only"},
)
raise ValueError(f"Unknown tool: {name}")
async def run():
"""Run the server."""
async with mcp.server.stdio.stdio\_server() as (read\_stream, write\_stream):
await server.run(
read\_stream,
write\_stream,
InitializationOptions(
server\_name="example",
server\_version="0.1.0",
capabilities=server.get\_capabilities(
notification\_options=NotificationOptions(),
experimental\_capabilities={},
),
),
)
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(run())
```
\_Full example: [examples/snippets/servers/lowlevel/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/direct\_call\_tool\_result.py)\_
\*\*Note:\*\* When returning `CallToolResult`, you bypass the automatic content/structured conversion. You must construct the complete response yourself.
### Pagination (Advanced)
For servers that need to handle large datasets, the low-level server provides paginated versions of list operations. This is an optional optimization - most servers won't need pagination unless they're dealing with hundreds or thousands of items.
#### Server-side Implementation
```python
"""
Example of implementing pagination with MCP server decorators.
"""
from pydantic import AnyUrl
import mcp.types as types
from mcp.server.lowlevel import Server
# Initialize the server
server = Server("paginated-server")
# Sample data to paginate
ITEMS = [f"Item {i}" for i in range(1, 101)] # 100 items
@server.list\_resources()
async def list\_resources\_paginated(request: types.ListResourcesRequest) -> types.ListResourcesResult:
"""List resources with pagination support."""
page\_size = 10
# Extract cursor from request params
cursor = request.params.cursor if request.params is not None else None
# Parse cursor to get offset
start = 0 if cursor is None else int(cursor)
end = start + page\_size
# Get page of resources
page\_items = [
types.Resource(uri=AnyUrl(f"resource://items/{item}"), name=item, description=f"Description for {item}")
for item in ITEMS[start:end]
]
# Determine next cursor
next\_cursor = str(end) if end < len(ITEMS) else None
return types.ListResourcesResult(resources=page\_items, nextCursor=next\_cursor)
```
\_Full example: [examples/snippets/servers/pagination\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/pagination\_example.py)\_
#### Client-side Consumption
```python
"""
Example of consuming paginated MCP endpoints from a client.
"""
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio\_client
from mcp.types import PaginatedRequestParams, Resource
async def list\_all\_resources() -> None:
"""Fetch all resources using pagination."""
async with stdio\_client(StdioServerParameters(command="uv", args=["run", "mcp-simple-pagination"])) as (
read,
write,
):
async with ClientSession(read, write) as session:
await session.initialize()
all\_resources: list[Resource] = []
cursor = None
while True:
# Fetch a page of resources
result = await session.list\_resources(params=PaginatedRequestParams(cursor=cursor))
all\_resources.extend(result.resources)
print(f"Fetched {len(result.resources)} resources")
# Check if there are more pages
if result.nextCursor:
cursor = result.nextCursor
else:
break
print(f"Total resources: {len(all\_resources)}")
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(list\_all\_resources())
```
\_Full example: [examples/snippets/clients/pagination\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/pagination\_client.py)\_
#### Key Points
- \*\*Cursors are opaque strings\*\* - the server defines the format (numeric offsets, timestamps, etc.)
- \*\*Return `nextCursor=None`\*\* when there are no more pages
- \*\*Backward compatible\*\* - clients that don't support pagination will still work (they'll just get the first page)
- \*\*Flexible page sizes\*\* - Each endpoint can define its own page size based on data characteristics
See the [simple-pagination example](examples/servers/simple-pagination) for a complete implementation.
### Writing MCP Clients
The SDK provides a high-level client interface for connecting to MCP servers using various [transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports):
```python
"""
cd to the `examples/snippets/clients` directory and run:
uv run client
"""
import asyncio
import os
from pydantic import AnyUrl
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio\_client
from mcp.shared.context import RequestContext
# Create server parameters for stdio connection
server\_params = StdioServerParameters(
command="uv", # Using uv to run the server
args=["run", "server", "fastmcp\_quickstart", "stdio"], # We're already in snippets dir
env={"UV\_INDEX": os.environ.get("UV\_INDEX", "")},
)
# Optional: create a sampling callback
async def handle\_sampling\_message(
context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
) -> types.CreateMessageResult:
print(f"Sampling request: {params.messages}")
return types.CreateMessageResult(
role="assistant",
content=types.TextContent(
type="text",
text="Hello, world! from model",
),
model="gpt-3.5-turbo",
stopReason="endTurn",
)
async def run():
async with stdio\_client(server\_params) as (read, write):
async with ClientSession(read, write, sampling\_callback=handle\_sampling\_message) as session:
# Initialize the connection
await session.initialize()
# List available prompts
prompts = await session.list\_prompts()
print(f"Available prompts: {[p.name for p in prompts.prompts]}")
# Get a prompt (greet\_user prompt from fastmcp\_quickstart)
if prompts.prompts:
prompt = await session.get\_prompt("greet\_user", arguments={"name": "Alice", "style": "friendly"})
print(f"Prompt result: {prompt.messages[0].content}")
# List available resources
resources = await session.list\_resources()
print(f"Available resources: {[r.uri for r in resources.resources]}")
# List available tools
tools = await session.list\_tools()
print(f"Available tools: {[t.name for t in tools.tools]}")
# Read a resource (greeting resource from fastmcp\_quickstart)
resource\_content = await session.read\_resource(AnyUrl("greeting://World"))
content\_block = resource\_content.contents[0]
if isinstance(content\_block, types.TextContent):
print(f"Resource content: {content\_block.text}")
# Call a tool (add tool from fastmcp\_quickstart)
result = await session.call\_tool("add", arguments={"a": 5, "b": 3})
result\_unstructured = result.content[0]
if isinstance(result\_unstructured, types.TextContent):
print(f"Tool result: {result\_unstructured.text}")
result\_structured = result.structuredContent
print(f"Structured tool result: {result\_structured}")
def main():
"""Entry point for the client script."""
asyncio.run(run())
if \_\_name\_\_ == "\_\_main\_\_":
main()
```
\_Full example: [examples/snippets/clients/stdio\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/stdio\_client.py)\_
Clients can also connect using [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http):
```python
"""
Run from the repository root:
uv run examples/snippets/clients/streamable\_basic.py
"""
import asyncio
from mcp import ClientSession
from mcp.client.streamable\_http import streamable\_http\_client
async def main():
# Connect to a streamable HTTP server
async with streamable\_http\_client("http://localhost:8000/mcp") as (
read\_stream,
write\_stream,
\_,
):
# Create a session using the client streams
async with ClientSession(read\_stream, write\_stream) as session:
# Initialize the connection
await session.initialize()
# List available tools
tools = await session.list\_tools()
print(f"Available tools: {[tool.name for tool in tools.tools]}")
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(main())
```
\_Full example: [examples/snippets/clients/streamable\_basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable\_basic.py)\_
### Client Display Utilities
When building MCP clients, the SDK provides utilities to help display human-readable names for tools, resources, and prompts:
```python
"""
cd to the `examples/snippets` directory and run:
uv run display-utilities-client
"""
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio\_client
from mcp.shared.metadata\_utils import get\_display\_name
# Create server parameters for stdio connection
server\_params = StdioServerParameters(
command="uv", # Using uv to run the server
args=["run", "server", "fastmcp\_quickstart", "stdio"],
env={"UV\_INDEX": os.environ.get("UV\_INDEX", "")},
)
async def display\_tools(session: ClientSession):
"""Display available tools with human-readable names"""
tools\_response = await session.list\_tools()
for tool in tools\_response.tools:
# get\_display\_name() returns the title if available, otherwise the name
display\_name = get\_display\_name(tool)
print(f"Tool: {display\_name}")
if tool.description:
print(f" {tool.description}")
async def display\_resources(session: ClientSession):
"""Display available resources with human-readable names"""
resources\_response = await session.list\_resources()
for resource in resources\_response.resources:
display\_name = get\_display\_name(resource)
print(f"Resource: {display\_name} ({resource.uri})")
templates\_response = await session.list\_resource\_templates()
for template in templates\_response.resourceTemplates:
display\_name = get\_display\_name(template)
print(f"Resource Template: {display\_name}")
async def run():
"""Run the display utilities example."""
async with stdio\_client(server\_params) as (read, write):
async with ClientSession(read, write) as session:
# Initialize the connection
await session.initialize()
print("=== Available Tools ===")
await display\_tools(session)
print("\n=== Available Resources ===")
await display\_resources(session)
def main():
"""Entry point for the display utilities client."""
asyncio.run(run())
if \_\_name\_\_ == "\_\_main\_\_":
main()
```
\_Full example: [examples/snippets/clients/display\_utilities.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/display\_utilities.py)\_
The `get\_display\_name()` function implements the proper precedence rules for displaying names:
- For tools: `title` > `annotations.title` > `name`
- For other objects: `title` > `name`
This ensures your client UI shows the most user-friendly names that servers provide.
### OAuth Authentication for Clients
The SDK includes [authorization support](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) for connecting to protected MCP servers:
```python
"""
Before running, specify running MCP RS server URL.
To spin up RS server locally, see
examples/servers/simple-auth/README.md
cd to the `examples/snippets` directory and run:
uv run oauth-client
"""
import asyncio
from urllib.parse import parse\_qs, urlparse
import httpx
from pydantic import AnyUrl
from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.streamable\_http import streamable\_http\_client
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken
class InMemoryTokenStorage(TokenStorage):
"""Demo In-memory token storage implementation."""
def \_\_init\_\_(self):
self.tokens: OAuthToken | None = None
self.client\_info: OAuthClientInformationFull | None = None
async def get\_tokens(self) -> OAuthToken | None:
"""Get stored tokens."""
return self.tokens
async def set\_tokens(self, tokens: OAuthToken) -> None:
"""Store tokens."""
self.tokens = tokens
async def get\_client\_info(self) -> OAuthClientInformationFull | None:
"""Get stored client information."""
return self.client\_info
async def set\_client\_info(self, client\_info: OAuthClientInformationFull) -> None:
"""Store client information."""
self.client\_info = client\_info
async def handle\_redirect(auth\_url: str) -> None:
print(f"Visit: {auth\_url}")
async def handle\_callback() -> tuple[str, str | None]:
callback\_url = input("Paste callback URL: ")
params = parse\_qs(urlparse(callback\_url).query)
return params["code"][0], params.get("state", [None])[0]
async def main():
"""Run the OAuth client example."""
oauth\_auth = OAuthClientProvider(
server\_url="http://localhost:8001",
client\_metadata=OAuthClientMetadata(
client\_name="Example MCP Client",
redirect\_uris=[AnyUrl("http://localhost:3000/callback")],
grant\_types=["authorization\_code", "refresh\_token"],
response\_types=["code"],
scope="user",
),
storage=InMemoryTokenStorage(),
redirect\_handler=handle\_redirect,
callback\_handler=handle\_callback,
)
async with httpx.AsyncClient(auth=oauth\_auth, follow\_redirects=True) as custom\_client:
async with streamable\_http\_client("http://localhost:8001/mcp", http\_client=custom\_client) as (read, write, \_):
async with ClientSession(read, write) as session:
await session.initialize()
tools = await session.list\_tools()
print(f"Available tools: {[tool.name for tool in tools.tools]}")
resources = await session.list\_resources()
print(f"Available resources: {[r.uri for r in resources.resources]}")
def run():
asyncio.run(main())
if \_\_name\_\_ == "\_\_main\_\_":
run()
```
\_Full example: [examples/snippets/clients/oauth\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/oauth\_client.py)\_
For a complete working example, see [`examples/clients/simple-auth-client/`](examples/clients/simple-auth-client/).
### Parsing Tool Results
When calling tools through MCP, the `CallToolResult` object contains the tool's response in a structured format. Understanding how to parse this result is essential for properly handling tool outputs.
```python
"""examples/snippets/clients/parsing\_tool\_results.py"""
import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio\_client
async def parse\_tool\_results():
"""Demonstrates how to parse different types of content in CallToolResult."""
server\_params = StdioServerParameters(
command="python", args=["path/to/mcp\_server.py"]
)
async with stdio\_client(server\_params) as (read, write):
async with ClientSession(read, write) as session:
await session.initialize()
# Example 1: Parsing text content
result = await session.call\_tool("get\_data", {"format": "text"})
for content in result.content:
if isinstance(content, types.TextContent):
print(f"Text: {content.text}")
# Example 2: Parsing structured content from JSON tools
result = await session.call\_tool("get\_user", {"id": "123"})
if hasattr(result, "structuredContent") and result.structuredContent:
# Access structured data directly
user\_data = result.structuredContent
print(f"User: {user\_data.get('name')}, Age: {user\_data.get('age')}")
# Example 3: Parsing embedded resources
result = await session.call\_tool("read\_config", {})
for content in result.content:
if isinstance(content, types.EmbeddedResource):
resource = content.resource
if isinstance(resource, types.TextResourceContents):
print(f"Config from {resource.uri}: {resource.text}")
elif isinstance(resource, types.BlobResourceContents):
print(f"Binary data from {resource.uri}")
# Example 4: Parsing image content
result = await session.call\_tool("generate\_chart", {"data": [1, 2, 3]})
for content in result.content:
if isinstance(content, types.ImageContent):
print(f"Image ({content.mimeType}): {len(content.data)} bytes")
# Example 5: Handling errors
result = await session.call\_tool("failing\_tool", {})
if result.isError:
print("Tool execution failed!")
for content in result.content:
if isinstance(content, types.TextContent):
print(f"Error: {content.text}")
async def main():
await parse\_tool\_results()
if \_\_name\_\_ == "\_\_main\_\_":
asyncio.run(main())
```
### MCP Primitives
The MCP protocol defines three core primitives that servers can implement:
| Primitive | Control | Description | Example Use |
|-----------|-----------------------|-----------------------------------------------------|------------------------------|
| Prompts | User-controlled | Interactive templates invoked by user choice | Slash commands, menu options |
| Resources | Application-controlled| Contextual data managed by the client application | File contents, API responses |
| Tools | Model-controlled | Functions exposed to the LLM to take actions | API calls, data updates |
### Server Capabilities
MCP servers declare capabilities during initialization:
| Capability | Feature Flag | Description |
|--------------|------------------------------|------------------------------------|
| `prompts` | `listChanged` | Prompt template management |
| `resources` | `subscribe`  
`listChanged`| Resource exposure and updates |
| `tools` | `listChanged` | Tool discovery and execution |
| `logging` | - | Server logging configuration |
| `completions`| - | Argument completion suggestions |
## Documentation
- [API Reference](https://modelcontextprotocol.github.io/python-sdk/api/)
- [Experimental Features (Tasks)](https://modelcontextprotocol.github.io/python-sdk/experimental/tasks/)
- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)
## Contributing
We are passionate about supporting contributors of all levels of experience and would love to see you get involved in the project. See the [contributing guide](CONTRIBUTING.md) to get started.
## License
This project is licensed under the MIT License - see the LICENSE file for details.