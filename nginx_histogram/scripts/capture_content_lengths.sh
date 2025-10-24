#!/bin/bash
set -euo pipefail

OUTPUT_FILE=${1:-/tmp/content-lengths.txt}

echo "Capturing content-length headers..."
echo "Output file: $OUTPUT_FILE"
echo "Press Ctrl+C to stop"

# Capture HTTP traffic and extract Content-Length headers
tcpdump -A -vvv -nli any '(port 80) and (length > 74)' -s 0 -w - 2>/dev/null | \
    strings | \
    grep -A10 HTTP | \
    grep Content-Length > "$OUTPUT_FILE"
