#!/bin/bash

# 5. Build docker image for training:
# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker rm
# Remove image if it exists
docker images | grep -q "hisolver-manim-training" && docker rmi hisolver-manim-training
# Build docker image
docker build -t hisolver-manim-training .

# 6. Tag image:
docker tag hisolver-manim-training gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest

# 7. Authenticate with GCP:
gcloud auth activate-service-account --key-file secrets/data-service-account.json

# 8. Push image to container registry
gcloud auth configure-docker
docker push gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest

# 9. Submit training job to vertex ai
gcloud ai custom-jobs create \
  --region=us-east4 \
  --display-name=hisolver-manim-training-job \
  --worker-pool-spec=machine-type=g2-standard-4,accelerator-type=NVIDIA_L4,accelerator-count=1,replica-count=1,container-image-uri=gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

# cpu
# --worker-pool-spec=machine-type=e2-standard-4,replica-count=1,container-image-uri=gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
