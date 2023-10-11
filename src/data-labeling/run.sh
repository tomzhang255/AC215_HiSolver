#!/bin/bash

# Create the network if we don't have it yet
docker network inspect hisolver-data-labeling-network >/dev/null 2>&1 || docker network create hisolver-data-labeling-network

# Build the image based on the Dockerfile
docker build -t hisolver-data-label-cli --platform=linux/arm64/v8 -f Dockerfile .

# Run All Containers
docker-compose run --rm --service-ports hisolver-data-label-cli

# Once the shell is exited, stop the specified container
docker stop hisolver-data-label-studio

# Prune dangling images
yes | docker image prune
