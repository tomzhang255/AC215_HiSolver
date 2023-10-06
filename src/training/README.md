- enable vertex ai: on gcp console, select project; search for it in search bar; find and "enable all recommended apis" on home page

- go to training/

- copy secrets/ from data-labeling/

- build and run docker container

- Run the following (to run training script locally):

```shell
cd ~/_DS/harvard/AC215/AC215_HiSolver/src/training
```

```shell
# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-training" && docker rmi hisolver-manim-training

# Build docker image
docker build -t hisolver-manim-training .

# Run training script in container
docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-training
```

BIG NOTE: this docker container setup is having trouble importing tensorflow from the python script... so we're not gonna use tf records... but in readme, give another reason...

Trying pytorch now... (first docker build takes ~10 min)

## serverless training with vertex ai

- gcp console - make sure container registry api is enabled

- install gc sdk

- in secrets folder create gcp_project_id.txt

- build docker image

```shell
# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-training" && docker rmi hisolver-manim-training

# Build docker image
docker build -t hisolver-manim-training .
```

- tag image

```shell
docker tag hisolver-manim-training gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

- authenticate with gcp (follow instructions)

```shell
gcloud auth login
```

- push image to container registry

```shell
gcloud auth configure-docker
docker push gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

- submit training job to vertex ai

```shell
gcloud ai custom-jobs create \
  --region=us_east4 \
  --display-name=hisolver-manim-training-job \
  --container-image-uri=gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest \
  --input-data-uri=gs://$(cat secrets/gcs_bucket_name.txt)/labeled \
  --output-data-uri=gs://$(cat secrets/gcs_bucket_name.txt)/output
```

updated syntax

```shell
gcloud ai custom-jobs create \
  --region=us-east4 \
  --display-name=hisolver-manim-training-job \
  --worker-pool-spec=machine-type=e2-standard-4,replica-count=1,container-image-uri=gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

- to monitor training status:

vertex ai - sidebar - model development section - training - select region us-east4 - you should see the job named: hisolver-manim-training-job
