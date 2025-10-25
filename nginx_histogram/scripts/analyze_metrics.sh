#!/bin/bash
set -euo pipefail

INPUT_FILE=${1:-/tmp/content-lengths.txt}

if [ ! -f "$INPUT_FILE" ]; then
  echo >&2 "Error: File $INPUT_FILE not found"
  exit 1
fi

TOTAL_LINES=$(wc -l "$INPUT_FILE" | awk '{ print $1 }')

if [ "$TOTAL_LINES" -eq 0 ]; then
  echo >&2 "No data found in $INPUT_FILE"
  exit 1
fi

echo >&2 "Analyzing $TOTAL_LINES content-length entries from $INPUT_FILE"
echo >&2 "================================================"

# Extract content lengths
cat "$INPUT_FILE" | cut -f2 -d':' | tr -d ' ' >/tmp/sizes.txt

# Max content length
MAX=$(sort -nr /tmp/sizes.txt | head -1)
echo >&2 "Max content length: $MAX bytes"

# Min content length
MIN=$(sort -n /tmp/sizes.txt | head -1)
echo >&2 "Min content length: $MIN bytes"

# Average content length
TOTAL_SIZE=$(paste -sd+ /tmp/sizes.txt | bc)
AVG=$(echo "scale=2; $TOTAL_SIZE / $TOTAL_LINES" | bc)
echo >&2 "Average content length: $AVG bytes"

# Sort for percentile calculations
sort -n /tmp/sizes.txt >/tmp/sorted_sizes.txt

# P50
# TODO - demo percentile calculation
target_percentile=50
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P50=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo >&2 "P50 content length: $P50 bytes"

# P90
target_percentile=90
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P90=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo >&2 "P90 content length: $P90 bytes"

# P99
target_percentile=99
target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
P99=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
echo >&2 "P99 content length: $P99 bytes"

# Cleanup
# rm -f /tmp/sizes.txt /tmp/sorted_sizes.txt
