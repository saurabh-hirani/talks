#!/bin/bash

echo "Cleaning up monitoring stack..."

# Delete VictoriaMetrics deployment
kubectl delete -f victoriametrics.yaml

# Delete node-exporter
kubectl delete -f node-exporter.yaml

# Delete Grafana
kubectl delete -f grafana.yaml

# Delete sample workload
kubectl delete -f workload.yaml

# Wait for pods to be terminated
echo "Waiting for pods to be terminated..."
kubectl wait --for=delete pod -l app=victoriametrics -n monitoring --timeout=60s 2>/dev/null || true
kubectl wait --for=delete pod -l app=vmagent -n monitoring --timeout=60s 2>/dev/null || true
kubectl wait --for=delete pod -l app=node-exporter -n monitoring --timeout=60s 2>/dev/null || true
kubectl wait --for=delete pod -l app=grafana -n monitoring --timeout=60s 2>/dev/null || true

echo "Cleanup complete!"
