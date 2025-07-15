"""
Simplified example for comparing files directly from command line arguments.
Usage: python simple_file_comparison.py file1.csv file2.csv
"""
import asyncio
import sys
import json
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

async def compare_files(file1_path, file2_path):
    """Compare two files using DeepDiff MCP."""
    # Use explicit transport configuration for reliability
    transport = StdioTransport(command="deepdiff-mcp", args=[])
    
    async with Client(transport=transport) as client:
        print(f"Comparing {file1_path} and {file2_path}...")
        
        # Call the compare_files tool
        result = await client.call_tool(
            "compare_files", 
            {
                "file1_path": file1_path, 
                "file2_path": file2_path,
                "ignore_order": True
            }
        )
        
        print("\nDifferences:")
        # Access the result data
        print(result)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python simple_file_comparison.py file1.csv file2.csv")
        sys.exit(1)
        
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    asyncio.run(compare_files(file1, file2))
