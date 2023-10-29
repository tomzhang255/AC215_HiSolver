#!/bin/bash

IMAGE_NAME=hisolver-manim-model-trainer
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets
export GCS_BUCKET_NAME=$(cat $SECRETS_DIR/gcs_bucket_name.txt)
export GCP_PROJECT=$(cat $SECRETS_DIR/gcp_project_id.txt)

docker login -u $(cat ../../secrets/docker_hub_username.txt) -p $(cat ../../secrets/docker_hub_token.txt)

docker pull tomzhang777/hisolver-manim-model-trainer

docker run --rm --name hisolver-manim-model-trainer-downloaded -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCP_PROJECT=$GCP_PROJECT \
tomzhang777/hisolver-manim-model-trainer
