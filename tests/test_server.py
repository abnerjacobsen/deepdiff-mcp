"""
Tests for the DeepDiff MCP server.
"""
import pytest
from fastmcp import Client

from deepdiff_mcp import create_server


@pytest.fixture
async def client():
    """Create an in-memory client connected to a DeepDiff MCP server."""
    server = create_server("Test Server")
    async with Client(server) as client:
        yield client


@pytest.mark.asyncio
async def test_list_tools(client):
    """Test that the server exposes the expected tools."""
    tools = await client.list_tools()
    tool_names = [tool.name for tool in tools]
    
    expected_tools = [
        "compare",
        "get_deep_distance",
        "search",
        "grep",
        "hash_object",
        "create_delta",
        "apply_delta",
        "extract_path",
    ]
    
    for tool_name in expected_tools:
        assert tool_name in tool_names


@pytest.mark.asyncio
async def test_compare(client):
    """Test the compare tool."""
    t1 = {"a": 1, "b": 2}
    t2 = {"a": 1, "b": 3}
    
    result = await client.call_tool("compare", {"t1": t1, "t2": t2})
    diff = result.json()
    
    assert "values_changed" in diff
    assert "root['b']" in diff["values_changed"]
    assert diff["values_changed"]["root['b']"]["old_value"] == 2
    assert diff["values_changed"]["root['b']"]["new_value"] == 3


@pytest.mark.asyncio
async def test_get_deep_distance(client):
    """Test the get_deep_distance tool."""
    t1 = {"a": 1, "b": 2}
    t2 = {"a": 1, "b": 3}
    
    result = await client.call_tool("get_deep_distance", {"t1": t1, "t2": t2})
    distance = float(result.text)
    
    assert 0 <= distance <= 1


@pytest.mark.asyncio
async def test_search(client):
    """Test the search tool."""
    obj = {"a": {"b": [1, 2, 3, {"c": "found me"}]}}
    
    result = await client.call_tool("search", {"obj": obj, "item": "found me"})
    search_result = result.json()
    
    assert "matched_values" in search_result
    assert "root['a']['b'][3]['c']" in search_result["matched_values"]


@pytest.mark.asyncio
async def test_extract_path(client):
    """Test the extract_path tool."""
    obj = {"a": {"b": [1, 2, 3, {"c": "value"}]}}
    
    result = await client.call_tool("extract_path", {"obj": obj, "path": "root['a']['b'][3]['c']"})
    
    assert result.text == "value"

@pytest.mark.asyncio
async def test_compare_files(client, tmp_path):
    """Test comparing files."""
    import os
    import pandas as pd
    
    # Create test files
    file1_path = os.path.join(tmp_path, "test1.csv")
    file2_path = os.path.join(tmp_path, "test2.csv")
    
    # Create sample DataFrames
    df1 = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    
    df2 = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 31, 35]  # Changed age for Bob
    })
    
    # Save to CSV
    df1.to_csv(file1_path, index=False)
    df2.to_csv(file2_path, index=False)
    
    # Test comparison
    result = await client.call_tool("compare_files", {
        "file1_path": file1_path,
        "file2_path": file2_path
    })
    
    diff = result.json()
    
    # We should have a difference in Bob's age
    assert "values_changed" in diff
    age_changes = [k for k in diff["values_changed"].keys() if "'age'" in k]
    assert len(age_changes) > 0
    
    # Check if one of the changes is Bob's age (value 30 -> 31)
    found_change = False
    for key in age_changes:
        change = diff["values_changed"][key]
        if change["old_value"] == 30 and change["new_value"] == 31:
            found_change = True
            break
    
    assert found_change, "Could not find the expected change in Bob's age"
