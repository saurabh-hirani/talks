#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 'promql_query' [-d 'time_ago']"
    echo "Examples:"
    echo "  $0 'rate(container_cpu_usage_seconds_total{pod=~\"cpu-memory-demo.*\"}[5m])'"
    echo "  $0 'node_cpu_seconds_total' -d '5 minutes ago'"
    echo "  $0 'container_memory_usage_bytes' -d '1 hour ago'"
    exit 1
fi

QUERY="$1"
VM_URL="http://localhost:8428"

# Check if -d option is provided
if [ "$2" = "-d" ] && [ -n "$3" ]; then
    # Convert date to Unix timestamp
    START_TIME=$(gdate -d "$3" +%s)
    END_TIME=$(gdate +%s)

    # URL encode the query
    ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

    # Query range data
    curl -s "$VM_URL/api/v1/query_range?query=$ENCODED_QUERY&start=$START_TIME&end=$END_TIME&step=60" | jq '.data.result[] | {metric: .metric, values: .values}'
else
    # URL encode the query
    ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

    # Query instant data
    curl -s "$VM_URL/api/v1/query?query=$ENCODED_QUERY" | jq '.data.result[] | {metric: .metric, value: .value[1]}'
fi
