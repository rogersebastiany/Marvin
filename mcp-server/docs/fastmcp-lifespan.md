> ## Documentation Index
> Fetch the complete documentation index at: https://gofastmcp.com/llms.txt
> Use this file to discover all available pages before exploring further.
> ## Feedback
> If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
> https://gofastmcp.com/\_mintlify/feedback/fastmcp/agent-feedback
>
> Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
>
> Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
# Lifespans
> Server-level setup and teardown with composable lifespans
export const VersionBadge = ({version}) => {
return 
New in version `{version}`
;
};
Lifespans let you run code once when the server starts and clean up when it stops. Unlike per-session handlers, lifespans run exactly once regardless of how many clients connect.
## Basic Usage
Use the `@lifespan` decorator to define a lifespan:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
@lifespan
async def app\_lifespan(server):
# Setup: runs once when server starts
print("Starting up...")
try:
yield {"started\_at": "2024-01-01"}
finally:
# Teardown: runs when server stops
print("Shutting down...")
mcp = FastMCP("MyServer", lifespan=app\_lifespan)
```
The dict you yield becomes the \*\*lifespan context\*\*, accessible from tools.
Always use `try/finally` for cleanup code to ensure it runs even if the server is cancelled.
## Accessing Lifespan Context
Access the lifespan context in tools via `ctx.lifespan\_context`:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP, Context
from fastmcp.server.lifespan import lifespan
@lifespan
async def app\_lifespan(server):
# Initialize shared state
data = {"users": ["alice", "bob"]}
yield {"data": data}
mcp = FastMCP("MyServer", lifespan=app\_lifespan)
@mcp.tool
def list\_users(ctx: Context) -> list[str]:
data = ctx.lifespan\_context["data"]
return data["users"]
```
## Composing Lifespans
Compose multiple lifespans with the `|` operator:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
@lifespan
async def config\_lifespan(server):
config = {"debug": True, "version": "1.0"}
yield {"config": config}
@lifespan
async def data\_lifespan(server):
data = {"items": []}
yield {"data": data}
# Compose with |
mcp = FastMCP("MyServer", lifespan=config\_lifespan | data\_lifespan)
```
Composed lifespans:
\* Enter in order (left to right)
\* Exit in reverse order (right to left)
\* Merge their context dicts (later values overwrite earlier on conflict)
## Backwards Compatibility
Existing `@asynccontextmanager` lifespans still work when passed directly to FastMCP:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from contextlib import asynccontextmanager
from fastmcp import FastMCP
@asynccontextmanager
async def legacy\_lifespan(server):
yield {"key": "value"}
mcp = FastMCP("MyServer", lifespan=legacy\_lifespan)
```
To compose an `@asynccontextmanager` function with `@lifespan` functions, wrap it with `ContextManagerLifespan`:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from contextlib import asynccontextmanager
from fastmcp.server.lifespan import lifespan, ContextManagerLifespan
@asynccontextmanager
async def legacy\_lifespan(server):
yield {"legacy": True}
@lifespan
async def new\_lifespan(server):
yield {"new": True}
# Wrap the legacy lifespan explicitly for composition
combined = ContextManagerLifespan(legacy\_lifespan) | new\_lifespan
```
## With FastAPI
When mounting FastMCP into FastAPI, use `combine\_lifespans` to run both your app's lifespan and the MCP server's lifespan:
```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.utilities.lifespan import combine\_lifespans
@asynccontextmanager
async def app\_lifespan(app):
print("FastAPI starting...")
yield
print("FastAPI shutting down...")
mcp = FastMCP("Tools")
mcp\_app = mcp.http\_app()
app = FastAPI(lifespan=combine\_lifespans(app\_lifespan, mcp\_app.lifespan))
app.mount("/mcp", mcp\_app)
```
See the [FastAPI integration guide](/integrations/fastapi#combining-lifespans) for full details.
Built with [Mintlify](https://mintlify.com).