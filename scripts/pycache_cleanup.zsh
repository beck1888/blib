#!/bin/zsh

# Step 1: Move one directory up
cd ..

# Step 2: Check if current directory is named 'blib'
if [[ "${PWD##*/}" != "blib" ]]; then
  echo "Error: This script must be run from inside the 'blib' directory."
  exit 1
fi

# Step 3: Recursively remove all __pycache__ directories and .pyc files
echo "Cleaning __pycache__ directories and .pyc files from: $PWD"

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null

# Remove .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null

echo "Cleanup complete."
