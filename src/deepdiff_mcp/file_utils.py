"""
Utilities for file operations in DeepDiff MCP.
"""
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd


def load_data_from_file(file_path: str) -> Any:
    """
    Load data from a file based on its extension.
    
    Args:
        file_path: Path to the file to load
        
    Returns:
        Data loaded from the file as a Python object
        
    Raises:
        ValueError: If the file type is unsupported
        FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == ".csv":
        return pd.read_csv(file_path).to_dict(orient="records")
    elif extension in [".xls", ".xlsx"]:
        return pd.read_excel(file_path).to_dict(orient="records")
    elif extension == ".json":
        return pd.read_json(file_path).to_dict(orient="records")
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def detect_delimiter(file_path: str) -> str:
    """
    Detect delimiter in a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Detected delimiter
    """
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        
    # Check common delimiters
    delimiters = [",", ";", "\t", "|"]
    counts = {delimiter: first_line.count(delimiter) for delimiter in delimiters}
    
    # Return the delimiter with the highest count
    return max(counts, key=counts.get)