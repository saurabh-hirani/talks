#!/bin/bash
set -euo pipefail

OUTPUT_FILE=${1:-/tmp/content-lengths.txt}

echo >&2 "Capturing content-length headers..."
echo >&2 "Output file: $OUTPUT_FILE"
echo >&2 "Press Ctrl+C to stop"

# Capture HTTP traffic and extract Content-Length headers
tcpdump -A -vvv -nli any '(port 80) and (length > 74)' -s 0 -w - 2>/dev/null |
  strings |
  grep -A10 HTTP |
  grep Content-Length >"$OUTPUT_FILE"
