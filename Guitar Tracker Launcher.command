#!/bin/bash

# Simple launcher for Classical Guitar Learning Tracker
# This creates a .command file that can be double-clicked on macOS

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the app directory
cd "$SCRIPT_DIR"

# Run the Python launcher
python3 launch.py