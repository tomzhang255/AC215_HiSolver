#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/secrets/
export GCP_PROJECT="ac-215"
export GCP_ZONE="us-central1-a"

# Create the network if we don't have it yet
docker network inspect data-versioning-network >/dev/null 2>&1 || docker network create data-versioning-network

# Build the image based on the Dockerfile
docker build -t hisolver-manim-data-version --platform=linux/arm64/v8 -f Dockerfile .

# Run Container
docker run --rm --name hisolver-manim-data-version -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/hisolver-data-collection-secrets.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e GCS_BUCKET_NAME=$(cat $SECRETS_DIR/gcs_bucket_name.txt) \
--network data-versioning-network hisolver-manim-data-version 