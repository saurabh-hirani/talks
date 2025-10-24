# Nginx Content-Length Analysis Demo

This setup demonstrates the scenario from the blog post about analyzing HTTP content-length metrics.

## Start the services

```bash
docker-compose up -d
```

## Demo Commands

### 1. Generate traffic (in traffic-generator container)

```bash
# Access the container
docker-compose exec traffic-generator sh

# Generate traffic with size range 100-1024 bytes
/scripts/generate_traffic.sh 100 1024

# Or generate larger payloads (simulate Prometheus metrics)
/scripts/generate_traffic.sh 1024 8192
```

### 2. Capture content-length headers (in nginx container)

```bash
# Access nginx container
docker-compose exec nginx sh

# Capture content-length data
/scripts/capture_content_lengths.sh /tmp/content-lengths.txt
```

### 3. Analyze metrics (in nginx container, after capturing data)

```bash
# Run analysis on captured data
/scripts/analyze_metrics.sh /tmp/content-lengths.txt
```

## Expected Output

```
Analyzing 150 content-length entries from /tmp/content-lengths.txt
================================================
Max content length: 1023 bytes
Min content length: 101 bytes
Average content length: 512.34 bytes
P50 content length: 511 bytes
P90 content length: 921 bytes
P99 content length: 1015 bytes
```

### 4. Generate percentile graphs (optional)

```bash
# Install tcpdump and bc
apk add --no-cache python3 python3-pip

# Install termgraph (if available)
pip install termgraph

# Generate percentile distribution (10%, 20%, 30%, etc.)
cat /tmp/content-lengths.txt | cut -f2 -d':' | tr -d ' ' | /scripts/percentile.sh $(seq 1 10 | while read p; do echo "$p * 10" | bc; done) | termgraph

# Or more granular (5%, 10%, 15%, etc.)
cat /tmp/content-lengths.txt | cut -f2 -d':' | tr -d ' ' | /scripts/percentile.sh $(seq 1 20 | while read p; do echo "$p * 5" | bc; done) | termgraph
```

## Stop the demo

```bash
docker-compose down
```
