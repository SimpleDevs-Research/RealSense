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
python "src/record2.py" "configs/depth_color_640x480x30.json" "recordings_ignore" -p