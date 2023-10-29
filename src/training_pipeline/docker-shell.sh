#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="hisolver-manim-fine-tuning"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets
export GCS_BUCKET_NAME=$(cat $SECRETS_DIR/gcs_bucket_name.txt)
export GCP_PROJECT=$(cat $SECRETS_DIR/gcp_project_id.txt)

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker stop && docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "$IMAGE_NAME" && docker rmi $IMAGE_NAME

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
# M1/2 chip macs use this line
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCP_PROJECT=$GCP_PROJECT \
$IMAGE_NAME
