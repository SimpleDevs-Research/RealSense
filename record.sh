#!/usr/bin/env bash

# --- Enter the RealSense project directory (adjust path if needed) ---
cd "$(dirname "$0")"

# --- Activate virtual environment ---
source ".venv/bin/activate"

# --- Generate timestamp: YYYYMMDD_HHMMSS ---
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# --- Ensure output directory exists ---
mkdir -p "recordings_ignore"

# --- Run the recording script with timestamped BAG file ---
python "src/record.py" "configs/depth_color.json" "recordings_ignore/${TIMESTAMP}.bag"