#!/bin/bash

# wait two mins to avoid errors on startup
sleep 2m

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Navigate to the script's directory
cd "$SCRIPT_DIR"
cd ..

# Activate the Python virtual environment
source venv/bin/activate

cd api
    
# Run the Python script
python main.py