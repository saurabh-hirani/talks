#!/bin/bash

echo "Deploying VictoriaMetrics and monitoring stack..."

# Deploy node-exporter
kubectl apply -f node-exporter.yaml

# Deploy VictoriaMetrics
kubectl apply -f victoriametrics.yaml

# Deploy Grafana
kubectl apply -f grafana.yaml

# Wait for node-exporter to be ready
echo "Waiting for node-exporter to be ready..."
kubectl wait --for=condition=ready pod -l app=node-exporter -n monitoring --timeout=300s

# Wait for VictoriaMetrics to be ready
echo "Waiting for VictoriaMetrics to be ready..."
kubectl wait --for=condition=ready pod -l app=victoriametrics -n monitoring --timeout=300s

# Wait for vmagent to be ready
echo "Waiting for vmagent to be ready..."
kubectl wait --for=condition=ready pod -l app=vmagent -n monitoring --timeout=300s

# Wait for Grafana to be ready
echo "Waiting for Grafana to be ready..."
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=300s

# Deploy sample workload
echo "Deploying sample workload..."
kubectl apply -f workload.yaml

# Get service URLs
VM_PORT=$(kubectl get svc victoriametrics -n monitoring -o jsonpath='{.spec.ports[0].nodePort}')
GRAFANA_PORT=$(kubectl get svc grafana -n monitoring -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)

echo ""
echo "Setup complete!"
echo "VictoriaMetrics UI: http://$MINIKUBE_IP:$VM_PORT"
echo "Grafana UI: http://$MINIKUBE_IP:$GRAFANA_PORT (admin/admin)"
echo ""
echo "Sample queries to try:"
echo "1. Node CPU usage: node_cpu_seconds_total"
echo "2. Node memory usage: node_memory_MemAvailable_bytes"
echo "3. Container CPU usage: container_cpu_usage_seconds_total"
echo "4. Container memory usage: container_memory_usage_bytes"
echo ""
echo "Port-forward commands:"
echo "VictoriaMetrics: kubectl port-forward -n monitoring svc/victoriametrics 8428:8428"
echo "Grafana: kubectl port-forward -n monitoring svc/grafana 3000:3000"
