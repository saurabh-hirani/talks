#!/bin/bash
set -euo pipefail

# Check if arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <min_size> <max_size>"
    echo "Example: $0 100 2048"
    exit 1
fi

MIN_SIZE=$1
MAX_SIZE=$2

# Validate inputs
if [ "$MIN_SIZE" -ge "$MAX_SIZE" ]; then
    echo "Error: min_size must be less than max_size"
    exit 1
fi

echo "Starting traffic generation..."
echo "Size range: ${MIN_SIZE}-${MAX_SIZE} bytes"
echo "Press Ctrl+C to stop"

while true; do
    # Generate random size between min and max
    SIZE=$(shuf -i ${MIN_SIZE}-${MAX_SIZE} -n 1)
    
    # Generate random data of that size
    DATA=$(head -c $SIZE /dev/urandom | base64 | tr -d '\n')
    
    # Pick random endpoint
    ENDPOINT=$(shuf -i 1-3 -n 1)
    
    # Send POST request
    curl -X POST "http://nginx/endpoint${ENDPOINT}/prometheus/write" \
         -H "Content-Type: application/x-protobuf" \
         -d "$DATA" \
         --max-time 5 \
         --silent || true
    
    echo "Sent ${SIZE} bytes to endpoint${ENDPOINT}"
    sleep 0.1
done
