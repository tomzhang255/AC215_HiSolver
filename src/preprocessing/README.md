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

1. Run this script to push image to docker hub:

```shell
./docker-hub.sh
```
