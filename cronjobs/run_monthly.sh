# !/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Navigate to the script's directory
cd "$SCRIPT_DIR"
cd ..

# Activate the Python virtual environment
source venv/bin/activate

cd cronjobs

python calculate_monthly_activity.py
