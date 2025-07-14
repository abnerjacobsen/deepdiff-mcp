"""
DeepDiff MCP Server

This package provides an MCP server that exposes DeepDiff functionality.
"""
from .server import DeepDiffMCP, create_server

__version__ = "0.1.0"
__all__ = ["DeepDiffMCP", "create_server"]
