"""
DeepDiff MCP Server

This module provides an MCP server that exposes DeepDiff functionality.
"""
from typing import Any, Dict, List, Optional, Union

from deepdiff import DeepDiff, DeepSearch, grep, extract
from deepdiff.delta import Delta
from deepdiff.deephash import DeepHash
from fastmcp import FastMCP, Context

class DeepDiffMCP:
    """MCP server for DeepDiff."""
    
    def __init__(self, name: str = "DeepDiff MCP"):
        """Initialize the DeepDiff MCP server."""
        self.mcp = FastMCP(name)
        self._register_tools()
        
    def _register_tools(self):
        """Register all available DeepDiff tools."""
        # DeepDiff tools
        self.mcp.tool(self.compare)
        self.mcp.tool(self.get_deep_distance)
        
        # DeepSearch tools
        self.mcp.tool(self.search)
        self.mcp.tool(self.grep)
        
        # DeepHash tools
        self.mcp.tool(self.hash_object)
        
        # Delta tools
        self.mcp.tool(self.create_delta)
        self.mcp.tool(self.apply_delta)
        
        # Extract tools
        self.mcp.tool(self.extract_path)
        
    def run(self, **kwargs):
        """Run the MCP server."""
        return self.mcp.run(**kwargs)
        
    def compare(
        self,
        t1: Any,
        t2: Any,
        ignore_order: bool = False,
        report_repetition: bool = False,
        exclude_paths: Optional[List[str]] = None,
        exclude_regex_paths: Optional[List[str]] = None,
        exclude_types: Optional[List[str]] = None,
        ignore_string_type_changes: bool = False,
        ignore_numeric_type_changes: bool = False,
        ignore_string_case: bool = False,
        significant_digits: Optional[int] = None,
        ctx: Optional[Context] = None,
    ) -> Dict:
        """
        Compare two objects and return their differences.
        
        Args:
            t1: First object to compare
            t2: Second object to compare
            ignore_order: Whether to ignore order in iterables
            report_repetition: Whether to report repetitions when ignore_order=True
            exclude_paths: Paths to exclude from comparison
            exclude_regex_paths: Regex paths to exclude from comparison
            exclude_types: Types to exclude from comparison
            ignore_string_type_changes: Whether to ignore string type changes
            ignore_numeric_type_changes: Whether to ignore numeric type changes
            ignore_string_case: Whether to ignore string case
            significant_digits: Number of significant digits to consider for float comparison
            ctx: MCP context
            
        Returns:
            Dictionary containing the differences
        """
        if ctx:
            ctx.info("Comparing objects...")
            
        # Convert exclude_types from string to actual types if provided
        actual_exclude_types = None
        if exclude_types:
            type_map = {
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "frozenset": frozenset,
                "bytes": bytes,
                "bytearray": bytearray,
                "complex": complex,
                "NoneType": type(None),
            }
            actual_exclude_types = [type_map.get(t, t) for t in exclude_types]
            
        diff = DeepDiff(
            t1=t1,
            t2=t2,
            ignore_order=ignore_order,
            report_repetition=report_repetition,
            exclude_paths=exclude_paths,
            exclude_regex_paths=exclude_regex_paths,
            exclude_types=actual_exclude_types,
            ignore_string_type_changes=ignore_string_type_changes,
            ignore_numeric_type_changes=ignore_numeric_type_changes,
            ignore_string_case=ignore_string_case,
            significant_digits=significant_digits,
        )
        
        if ctx:
            ctx.info(f"Found {len(diff)} differences")
            
        return diff.to_dict()
    
    def get_deep_distance(
        self,
        t1: Any,
        t2: Any,
        ignore_order: bool = False,
        ctx: Optional[Context] = None,
        **kwargs
    ) -> float:
        """
        Get the deep distance between two objects.
        
        Args:
            t1: First object
            t2: Second object
            ignore_order: Whether to ignore order in iterables
            ctx: MCP context
            **kwargs: Additional arguments for DeepDiff
            
        Returns:
            Float representing the deep distance (between 0 and 1)
        """
        if ctx:
            ctx.info("Calculating deep distance...")
            
        diff = DeepDiff(t1=t1, t2=t2, ignore_order=ignore_order, **kwargs)
        distance = diff.get_deep_distance()
        
        if ctx:
            ctx.info(f"Deep distance: {distance}")
            
        return distance
    
    def search(
        self,
        obj: Any,
        item: Any,
        case_sensitive: bool = False,
        exact_match: bool = False,
        ctx: Optional[Context] = None,
    ) -> Dict:
        """
        Search for an item in an object.
        
        Args:
            obj: Object to search in
            item: Item to search for
            case_sensitive: Whether the search is case-sensitive
            exact_match: Whether to perform an exact match
            ctx: MCP context
            
        Returns:
            Dictionary containing search results
        """
        if ctx:
            ctx.info(f"Searching for {item}...")
            
        result = DeepSearch(
            obj=obj,
            item=item,
            case_sensitive=case_sensitive,
            exact_match=exact_match,
        )
        
        if ctx:
            paths_count = sum(len(paths) for paths in result.values())
            ctx.info(f"Found {paths_count} matches")
            
        return result
    
    def grep(
        self,
        obj: Any,
        item: Any,
        case_sensitive: bool = False,
        exact_match: bool = False,
        ctx: Optional[Context] = None,
    ) -> Dict:
        """
        Grep for an item in an object.
        
        Args:
            obj: Object to grep in
            item: Item to grep for
            case_sensitive: Whether the grep is case-sensitive
            exact_match: Whether to perform an exact match
            ctx: MCP context
            
        Returns:
            Dictionary containing grep results
        """
        if ctx:
            ctx.info(f"Grepping for {item}...")
            
        result = grep(
            obj=obj,
            item=item,
            case_sensitive=case_sensitive,
            exact_match=exact_match,
        )
        
        if ctx:
            paths_count = sum(len(paths) for paths in result.values())
            ctx.info(f"Found {paths_count} matches")
            
        return result
    
    def hash_object(
        self,
        obj: Any,
        exclude_types: Optional[List[str]] = None,
        exclude_paths: Optional[List[str]] = None,
        exclude_regex_paths: Optional[List[str]] = None,
        ctx: Optional[Context] = None,
    ) -> Dict:
        """
        Hash an object based on its content.
        
        Args:
            obj: Object to hash
            exclude_types: Types to exclude from hashing
            exclude_paths: Paths to exclude from hashing
            exclude_regex_paths: Regex paths to exclude from hashing
            ctx: MCP context
            
        Returns:
            Dictionary mapping objects to their hashes
        """
        if ctx:
            ctx.info("Hashing object...")
            
        # Convert exclude_types from string to actual types if provided
        actual_exclude_types = None
        if exclude_types:
            type_map = {
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "frozenset": frozenset,
                "bytes": bytes,
                "bytearray": bytearray,
                "complex": complex,
                "NoneType": type(None),
            }
            actual_exclude_types = [type_map.get(t, t) for t in exclude_types]
            
        hasher = DeepHash(
            obj,
            exclude_types=actual_exclude_types,
            exclude_paths=exclude_paths,
            exclude_regex_paths=exclude_regex_paths,
        )
        
        # Convert the DeepHash object to a dict for serialization
        # We only return the hash of the root object as the full hasher 
        # contains references to all sub-objects which may not be serializable
        result = {"hash": hasher[obj]}
        
        if ctx:
            ctx.info("Hash calculated successfully")
            
        return result
    
    def create_delta(
        self,
        t1: Any,
        t2: Any,
        ctx: Optional[Context] = None,
        **kwargs
    ) -> Dict:
        """
        Create a delta that can be used to transform t1 into t2.
        
        Args:
            t1: Source object
            t2: Target object
            ctx: MCP context
            **kwargs: Additional arguments for DeepDiff
            
        Returns:
            Serializable delta representation
        """
        if ctx:
            ctx.info("Creating delta...")
            
        diff = DeepDiff(t1=t1, t2=t2, **kwargs)
        delta = Delta(diff)
        
        # Convert to a serializable format
        return delta.to_dict()
    
    def apply_delta(
        self,
        obj: Any,
        delta_dict: Dict,
        ctx: Optional[Context] = None,
    ) -> Any:
        """
        Apply a delta to an object.
        
        Args:
            obj: Object to transform
            delta_dict: Delta dictionary created by create_delta
            ctx: MCP context
            
        Returns:
            Transformed object
        """
        if ctx:
            ctx.info("Applying delta...")
            
        delta = Delta(delta_dict)
        result = obj + delta
        
        if ctx:
            ctx.info("Delta applied successfully")
            
        return result
    
    def extract_path(
        self,
        obj: Any,
        path: str,
        ctx: Optional[Context] = None,
    ) -> Any:
        """
        Extract a value from an object using a path.
        
        Args:
            obj: Object to extract from
            path: Path to extract
            ctx: MCP context
            
        Returns:
            Extracted value
        """
        if ctx:
            ctx.info(f"Extracting path: {path}")
            
        result = extract(obj, path)
        
        if ctx:
            ctx.info("Extraction completed")
            
        return result


def create_server(name: str = "DeepDiff MCP") -> DeepDiffMCP:
    """Create a new DeepDiff MCP server."""
    return DeepDiffMCP(name)
