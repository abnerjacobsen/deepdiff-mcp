"""
Command-line interface for the DeepDiff MCP server.
"""
import argparse
import sys
from typing import List, Optional

from .server import create_server


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="DeepDiff MCP Server")
    
    parser.add_argument(
        "--name", 
        type=str, 
        default="DeepDiff MCP",
        help="Name of the MCP server"
    )
    
    parser.add_argument(
        "--transport", 
        type=str, 
        default="stdio",
        choices=["stdio", "http", "sse"],
        help="Transport protocol to use"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1",
        help="Host to bind to (for HTTP and SSE transports)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind to (for HTTP and SSE transports)"
    )
    
    parser.add_argument(
        "--path", 
        type=str, 
        default="/mcp",
        help="Path to serve on (for HTTP transport)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Run the DeepDiff MCP server."""
    parsed_args = parse_args(args)
    
    server = create_server(name=parsed_args.name)
    
    transport_kwargs = {}
    if parsed_args.transport in ["http", "sse"]:
        transport_kwargs.update(
            host=parsed_args.host,
            port=parsed_args.port,
        )
    
    if parsed_args.transport == "http":
        transport_kwargs["path"] = parsed_args.path
    
    try:
        server.run(transport=parsed_args.transport, **transport_kwargs)
        return 0
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
