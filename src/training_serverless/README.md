# LLM Fine-tuning

## I. Note

This directory is self-contained demonstration of serverless training with Vertex AI. It is not part of the final Vertex AI pipeline. The training component to be used in the final pipeline is in `src/training_pipeline/`.

## II. Check work

Make sure you've followed all the steps from the data pre-processing section `src/data-labeling/README.md`.

## III. Training-related setup

1. Traverse to the correct directory: `src/training`

2. Copy the `secrets/` folder from `src/data-labeling/` so it now has a copy at `src/training/secrets/`

## IV. [Optional] Run training script locally

1. Run the following to test-run the training script in a local docker container:

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

## V. Serverless training with Vertex AI

1. Go to Google Cloud Platform Console -> select your project -> search for "Vertex AI" in the search bar -> Click "ENABLE ALL RECOMMENDED APIS" on the home page

2. Still on the console -> search for "Container Registry" in the search bar -> make sure the Container Registry API is enabled

3. Install Google Cloud SDK on your local machine (https://cloud.google.com/sdk/docs/install)

4. In `src/training/secrets/` create a file named `gcp_project_id.txt` and put the GCP Project ID that you've been using in it

5. Build docker image for training:

```shell
# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-training" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-training" && docker rmi hisolver-manim-training

# Build docker image
docker build -t hisolver-manim-training .
```

6. Tag image:

```shell
docker tag hisolver-manim-training gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

7. Authenticate with GCP (follow instructions; it should ask you to log-in on your browser)

```shell
gcloud auth login
```

8. Push image to container registry

```shell
gcloud auth configure-docker
docker push gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

9. Submit training job to vertex ai

```shell
gcloud ai custom-jobs create \
  --region=us-east4 \
  --display-name=hisolver-manim-training-job \
  --worker-pool-spec=machine-type=e2-standard-4,replica-count=1,container-image-uri=gcr.io/$(cat secrets/gcp_project_id.txt)/hisolver-manim-training:latest
```

10. To monitor training status:

- On the GCP console -> search for "Vertex AI" with the search bar
- On the Vertex AI page -> look at the sidebar -> look for the "MODEL DEVELOPMENT" section -> select "Training"
- On the Training page -> select region "us-east4" as we previously specified in the above command
- You should then see your job named: "hisolver-manim-training-job"
