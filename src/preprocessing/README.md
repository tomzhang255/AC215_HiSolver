# Data Pre-processing

## I. Check work

Make sure you've followed all the steps from the data collection section `src/collection/README.md`.

## II. Run data pre-processing script in a docker contianer

1. Start a Docker daemon (i.e., open up Docker Desktop)

2. Traverse to the correct directory: `src/preprocessing/`

3. Build and run docker container: `./docker-shell.sh`

4. Once container starts running, it should bring up a shell prompt; in it, run: `python preprocess.py`

5. The pre-processing script should be running; if you go to your bucket page again on GCP, you should see the bucket being populated with processed JSON files in the `processed/` folder

6. In case you need to rebuild the container, just rerun step 3

## III. Push image to docker hub

1. Login to the hub:

```shell
docker login -u $(cat ../../secrets/docker_hub_username.txt) -p $(cat ../../secrets/docker_hub_token.txt)
```

2. Build and tag the image:

```shell
docker build -t $(cat ../../secrets/docker_hub_username.txt)/hisolver-manim-data-processor --platform=linux/amd64/v2 -f Dockerfile .
```

3. Push to docker hub:

```shell
docker push $(cat ../../secrets/docker_hub_username.txt)/hisolver-manim-data-processor
```
