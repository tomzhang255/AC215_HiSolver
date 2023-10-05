- enable vertex ai: on gcp console, select project; search for it in search bar; find and "enable all recommended apis" on home page

- go to training/

- copy secrets/ from data-labeling/

- build and run docker container

- Run the following:

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
