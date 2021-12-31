#!/usr/bin/bash

docker stop rps_db
docker stop rps_webserver
docker compose rm -f -v 

# docker compose build --no-cache


docker compose up -d
