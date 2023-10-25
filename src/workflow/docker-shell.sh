#!/bin/bash

# set -e

export IMAGE_NAME="hisolver-manim-workflow"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets
export GCS_BUCKET_NAME=$(cat $SECRETS_DIR/gcs_bucket_name.txt)
export GCP_PROJECT=$(cat $SECRETS_DIR/gcp_project_id.txt)
export GITHUB_PAT=$(cat $SECRETS_DIR/pat.txt)
export GCS_SERVICE_ACCOUNT=$(cat $SECRETS_DIR/gcs_service_account.txt)
export GCP_REGION="us-east4"
export GCS_PACKAGE_URI="gs://$GCS_BUCKET_NAME"
export DOCKER_HUB_USERNAME=$(cat $SECRETS_DIR/docker_hub_username.txt)

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker stop && docker ps -a --filter "ancestor=$IMAGE_NAME" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "$IMAGE_NAME" && docker rmi $IMAGE_NAME

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$BASE_DIR/../collection":/data-collector \
-v "$BASE_DIR/../preprocessing":/data-processor \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
-e GCP_REGION=$GCP_REGION \
-e GCS_PACKAGE_URI=$GCS_PACKAGE_URI \
-e GITHUB_PAT=$GITHUB_PAT \
-e DOCKER_HUB_USERNAME=$DOCKER_HUB_USERNAME \
$IMAGE_NAME
