#!/bin/bash
set -euo pipefail

INPUT_FILE=${1:-/tmp/content-lengths.txt}

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE not found"
    exit 1
fi

TOTAL_LINES=$(wc -l "$INPUT_FILE" | awk '{ print $1 }')

if [ "$TOTAL_LINES" -eq 0 ]; then
    echo "No data found in $INPUT_FILE"
    exit 1
fi

echo "Analyzing $TOTAL_LINES content-length entries from $INPUT_FILE"
echo "================================================"

# Extract content lengths
cat "$INPUT_FILE" | cut -f2 -d':' | tr -d ' ' > /tmp/sizes.txt

# Max content length
MAX=$(sort -nr /tmp/sizes.txt | head -1)
echo "Max content length: $MAX bytes"

# Min content length  
MIN=$(sort -n /tmp/sizes.txt | head -1)
echo "Min content length: $MIN bytes"

# Average content length
TOTAL_SIZE=$(paste -sd+ /tmp/sizes.txt | bc)
AVG=$(echo "scale=2; $TOTAL_SIZE / $TOTAL_LINES" | bc)
echo "Average content length: $AVG bytes"

# Sort for percentile calculations
sort -n /tmp/sizes.txt > /tmp/sorted_sizes.txt

# P50
target_percentile=50
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P50=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo "P50 content length: $P50 bytes"

# P90
target_percentile=90
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P90=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo "P90 content length: $P90 bytes"

# P99
target_percentile=99
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P99=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo "P99 content length: $P99 bytes"

# Cleanup
rm -f /tmp/sizes.txt /tmp/sorted_sizes.txt
