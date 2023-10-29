#!/bin/bash

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-training" && docker rmi hisolver-manim-training

# Build docker image
docker build -t hisolver-manim-training .

# Run training script in container
docker run -v ./secrets/data-service-account.json:/secrets/data-service-account.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-training
