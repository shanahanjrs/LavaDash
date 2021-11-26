#!/bin/bash

# Check docker is running
if [[ $(ps aux | grep docker | grep -v grep | wc -l | xargs) < 1 ]]; then
    echo "ERROR docker must be running..."
    exit 1
fi

set -x

# Start these without attaching
docker-compose up -d influxdb chronograf grafana redis

# Start these and attach
docker-compose up scraper analyzer django

set +x
