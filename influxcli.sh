#!/bin/bash

echo '===> Common commands:'
echo '===>   create database analyses'
echo '===>   use analyses'
echo '===>   select "polarity", "author", "type" from "analysis_event"'
echo

set -x

docker-compose exec influxdb influx

set +x
