# Data Pre-processing

## I. Check work

Make sure you've followed all the steps from the data collection section `src/collection/README.md`.

## II. Run data pre-processing script in a docker contianer

1. Copy the `secrets` folder from `src/collection/secrets/` and paste it to `src/preprocessing/secrets`

2. Traverse to the correct directory: `src/preprocessing/`

3. Remove all containers built from this image if such containers exist

```
docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-preprocessing" -q | xargs docker rm
```

4. Remove image if it exists

```
docker images | grep -q "hisolver-manim-preprocessing" && docker rmi hisolver-manim-preprocessing
```

5. Build docker image

```
docker build -t hisolver-manim-preprocessing .
```

6. Run collection script in container

```
docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt) hisolver-manim-preprocessing
```
