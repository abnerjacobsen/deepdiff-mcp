# DeepDiff MCP Server

An MCP (Model Context Protocol) server for the [DeepDiff](https://github.com/seperman/deepdiff) library. This server allows you to use DeepDiff functionality through the Model Context Protocol, enabling interaction with DeepDiff from any MCP client.

## Installation

### Using pip

```bash
pip install deepdiff-mcp
```

### Using uv (recommended)

```bash
uv pip install deepdiff-mcp
```

## Usage

### Running the server

You can run the DeepDiff MCP server in several ways:

#### As a command-line tool

```bash
# Using stdio transport (default)
deepdiff-mcp

# Using HTTP transport
deepdiff-mcp --transport http --host 127.0.0.1 --port 8000

# Using SSE transport
deepdiff-mcp --transport sse --host 127.0.0.1 --port 8000
```

#### As a Python module

```python
from deepdiff_mcp import create_server

# Create a DeepDiff MCP server
server = create_server("My DeepDiff Server")

# Run the server with stdio transport (default)
server.run()

# Or with HTTP transport
server.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")

# Or with SSE transport
server.run(transport="sse", host="127.0.0.1", port=8000)
```

### Connecting to the server

You can connect to the server using any MCP client. Here's an example using FastMCP:

```python
import asyncio
from fastmcp import Client

async def main():
    # Connect to a DeepDiff MCP server running as a subprocess
    async with Client("deepdiff-mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Compare two dictionaries
        t1 = {"a": 1, "b": 2}
        t2 = {"a": 1, "b": 3, "c": 4}
        
        result = await client.call_tool("compare", {"t1": t1, "t2": t2})
        print(f"Differences: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Available Tools

The DeepDiff MCP server provides the following tools:

- `compare` - Compare two objects and return their differences
- `get_deep_distance` - Calculate the deep distance between two objects
- `search` - Search for an item within an object
- `grep` - Search for an item within an object using grep-like behavior
- `hash_object` - Hash an object based on its contents
- `create_delta` - Create a delta that can transform one object into another
- `apply_delta` - Apply a delta to transform an object
- `extract_path` - Extract a value from an object using a path

## Documentation

For more information about DeepDiff, see the [DeepDiff documentation](https://zepworks.com/deepdiff/current/).

For more information about MCP and FastMCP, see the [Model Context Protocol](https://modelcontextprotocol.io/) and [FastMCP documentation](https://gofastmcp.com/).
