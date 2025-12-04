#!/bin/bash
# RICK DIFF SAVER
# Usage: ./save_diff.sh <file_path> <description>
# Saves a diff of the current file state vs HEAD to a log folder before changes are applied.

FILE_PATH=$1
DESC=$2
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="logs/diffs"

mkdir -p "$LOG_DIR"

if [ -z "$FILE_PATH" ]; then
    echo "Usage: ./save_diff.sh <file_path> <description>"
    exit 1
fi

FILENAME=$(basename "$FILE_PATH")
DIFF_FILE="$LOG_DIR/${TIMESTAMP}_${FILENAME}.diff"

echo "Saving diff for $FILE_PATH..."
git diff HEAD -- "$FILE_PATH" > "$DIFF_FILE"

# Add metadata
echo "# Description: $DESC" >> "$DIFF_FILE"
echo "# Timestamp: $TIMESTAMP" >> "$DIFF_FILE"

echo "Diff saved to $DIFF_FILE"
