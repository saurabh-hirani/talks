#!/bin/bash
set -euo pipefail

# Read data from stdin
data=$(cat)
total_lines=$(echo "$data" | wc -l)

# Sort the data
sorted_data=$(echo "$data" | sort -n)

# Calculate percentiles for each argument and output in termgraph format
for percentile in "$@"; do
  target_line=$(echo "$percentile * $total_lines / 100" | bc)
  value=$(echo "$sorted_data" | sed -n "${target_line}p")
  echo "P${percentile} $value"
done
