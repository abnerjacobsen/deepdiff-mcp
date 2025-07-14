"""
Example showing how to use the DeepDiff MCP client.
"""
import asyncio
from fastmcp import Client

async def main():
    # Create an MCP client to connect to our server
    # This assumes the server is running from the server_example.py script
    async with Client("python examples/server_example.py") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Example: Compare two dictionaries
        t1 = {"a": 1, "b": 2, "c": 3}
        t2 = {"a": 1, "b": 4, "c": 3, "d": 5}
        
        print("\nComparing dictionaries:")
        print(f"t1 = {t1}")
        print(f"t2 = {t2}")
        
        result = await client.call_tool("compare", {"t1": t1, "t2": t2})
        print("\nDifferences:")
        print(result.text)
        
        # Example: Get deep distance
        distance_result = await client.call_tool("get_deep_distance", {"t1": t1, "t2": t2})
        print(f"\nDeep distance: {distance_result.text}")
        
        # Example: Search for a value
        search_obj = {"a": {"b": [1, 2, 3, {"c": "found me"}]}}
        search_result = await client.call_tool("search", {"obj": search_obj, "item": "found me"})
        print("\nSearch result:")
        print(search_result.text)

if __name__ == "__main__":
    asyncio.run(main())
