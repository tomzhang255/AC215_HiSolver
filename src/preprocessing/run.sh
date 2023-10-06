#!/bin/bash

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-preprocessing" && docker rmi hisolver-manim-preprocessing

# Build docker image
docker build -t hisolver-manim-preprocessing .

# Run pre-processing script in container
# docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-preprocessing
docker run \
  -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json \
  -v $(pwd)/../../.dvc:/app/.dvc \
  -v $(pwd)/../../.git:/app/.git \
  -v ~/.ssh:/root/.ssh \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json \
  -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) \
  -e DVC_REMOTE_NAME=$(cat secrets/dvc_remote_name.txt) \
  hisolver-manim-preprocessing