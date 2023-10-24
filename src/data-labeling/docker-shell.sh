#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="hisolver-data-label-cli"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets
export GCS_BUCKET_NAME=$(cat $SECRETS_DIR/gcs_bucket_name.txt)
export GCP_PROJECT=$(cat $SECRETS_DIR/gcp_project_id.txt)
export GITHUB_PAT=$(cat $SECRETS_DIR/pat.txt)

# Create the network if we don't have it yet
docker network inspect hisolver-data-labeling-network >/dev/null 2>&1 || docker network create hisolver-data-labeling-network

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker stop && docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "$IMAGE_NAME" && docker rmi $IMAGE_NAME

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
# M1/2 chip macs use this line
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run All Containers
docker-compose run --rm --service-ports $IMAGE_NAME

# Once the shell is exited, stop the specified container
docker stop hisolver-data-label-studio

# Prune dangling images
yes | docker image prune
