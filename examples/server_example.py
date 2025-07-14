"""
Example showing how to use the DeepDiff MCP server.
"""
from deepdiff_mcp import create_server

if __name__ == "__main__":
    # Create a DeepDiff MCP server
    server = create_server("DeepDiff Example")
    
    # Run the server using stdio transport (default)
    server.run()
