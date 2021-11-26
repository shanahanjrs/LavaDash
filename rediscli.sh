#!/bin/bash

set -x

docker-compose exec redis redis-cli

set +x
