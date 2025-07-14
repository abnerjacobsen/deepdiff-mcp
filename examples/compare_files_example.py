"""
Example showing how to compare two files using DeepDiff MCP.
"""
import asyncio
import os
import sys
import tempfile
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

# Create sample CSV files for demonstration
def create_sample_files():
    """Create sample CSV files for testing."""
    
    file1_content = """id,name,age,city
1,John,30,New York
2,Jane,25,Los Angeles
3,Bob,40,Chicago
"""
    
    file2_content = """id,name,age,city
1,John,30,New York
2,Jane,27,Los Angeles
3,Bob,40,San Francisco
4,Alice,35,Dallas
"""
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Write sample files
    file1_path = os.path.join(temp_dir, "data1.csv")
    with open(file1_path, "w") as f:
        f.write(file1_content)
        
    file2_path = os.path.join(temp_dir, "data2.csv")
    with open(file2_path, "w") as f:
        f.write(file2_content)
        
    return file1_path, file2_path


async def main():
    # Create sample files
    file1_path, file2_path = create_sample_files()
    print(f"Created sample files:\n  {file1_path}\n  {file2_path}")
    
    # Path to the server script (adjust as needed)
    server_script = os.path.join(os.path.dirname(__file__), "server_example.py")
    
    # Create an MCP client to connect to our server - Using explicit StdioTransport
    print("Connecting to DeepDiff MCP server...")
    
    # Método 1: Especificando explicitamente o transporte com args como lista
    transport = StdioTransport(command="python", args=[server_script])
    async with Client(transport=transport) as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        print("\nComparing CSV files...")
        result = await client.call_tool(
            "compare_files", 
            {
                "file1_path": file1_path, 
                "file2_path": file2_path,
                "ignore_order": True
            }
        )
        
        print("\nDifferences between files:")
        print(result.text)
        
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
