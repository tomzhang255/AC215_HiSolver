# Data Pre-processing

## I. Check work

Make sure you've followed all the steps from the data collection section `src/collection/README.md`.

## II. Run data pre-processing script in a docker contianer

1. Start a Docker daemon (i.e., open up Docker Desktop)

2. Copy the `secrets` folder from `src/collection/secrets/` and paste it to `src/preprocessing/secrets`

3. Traverse to the correct directory: `src/preprocessing/`

4. Run the following:

```shell
# Remove all containers built from this image if such containers exist
docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker rm

# Remove image if it exists
docker images | grep -q "hisolver-manim-preprocessing" && docker rmi hisolver-manim-preprocessing

# Build docker image
docker build -t hisolver-manim-preprocessing .

# Run pre-processing script in container
docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-preprocessing
```

5. The pre-processing script should be running; if you go to your bucket page again on GCP, you should see the bucket being populated with processed JSON files in the `processed/` folder

6. In case you need to rebuild the container, just rerun step 4
