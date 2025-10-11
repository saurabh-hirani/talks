#!/bin/bash

set -eou pipefail

# Start minikube with minimal resources
echo "Starting minikube..."
minikube start --cpus=2 --memory=2048 --driver=docker

# Enable metrics-server addon
echo "Enabling metrics-server..."
minikube addons enable metrics-server

# Wait for metrics-server to be ready
echo "Waiting for metrics-server to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=metrics-server -n kube-system --timeout=300s

echo "Setup complete! Minikube is running with metrics-server enabled."
