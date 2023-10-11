#!/bin/bash

# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-collection" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-collection" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-collection" && docker rmi hisolver-manim-collection

# Build docker image
docker build -t hisolver-manim-collection .

# Run collection script in container
docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GITHUB_PAT=$(cat secrets/pat.txt) -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-collection
