#!/usr/bin/env bash
set -x
set -e

task_name="icinga-demo-$(date +%s)"
base_image="$(grep '^FROM' Dockerfile | awk '{ print $2 }')"

docker pull "$base_image"
docker build -t "$task_name" -f "$dockerfile" .
docker run --privileged=true -p 8080:80 -p 4567:4567 -p 6315:6315  -v /data/icinga:/shared -i -t $task_name /bin/bash -c '/opt/monitoring-transition/bin/start.sh && /bin/bash'
