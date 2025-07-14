#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Install the package in development mode
echo "Installing package in development mode..."
uv pip install -e .

echo "Installation complete."
