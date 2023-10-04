# Data Versioning

This Python-scripted Docker container is orchestrated to securely download and manage processed data from a designated processed folder in the Google Cloud Storage bucket, aimed at implementing Data Version Control (DVC) on the cloud. Initiated by a shell script, the container interfaces with the Google Cloud environment, pulling relevant data blobs and ensuring their organized local placement, thus facilitating streamlined, secure, and orderly data retrieval and versioning workflows within cloud-based storage solutions.

## I. Check work

Make sure you've followed all the steps from the data collection section `src/collection/README.md`.

## II. Create a Data Store folder in GCS Bucket

1. Go to https://console.cloud.google.com/storage/browser

2. Go to the bucket hisolver-data-collection-2 (change to your bucketname)

3. Create a folder dvc_store inside the bucket

## III. Run data data versioning script in a docker container

1. Start a Docker daemon (i.e., open up Docker Desktop)

2. Copy the `secrets` folder from `src/collection/secrets/` and paste it to `src/data-versioning/secrets`

3. Traverse to the correct directory: `src/data-versioning/`

4. Remove all containers built from this image if such containers exist

```shell
docker ps -a --filter "ancestor=hisolver-manim-data-version" -q | xargs docker stop && docker ps -a --filter "ancestor=hisolver-manim-data-version" -q | xargs docker rm
```

5. Remove image if it exists

```shell
docker images | grep -q "hisolver-manim-data-version" && docker rmi hisolver-manim-data-version
```

6. Run the Docker shell file - this will build and run the docker and execute the data_versioning.py scrip

```shell
./docker-shell.sh
```

7. Initialize a git repo - we need this to create the DVC init

```shell
git init
```

8. Initialize the Data registry

```shell
dvc init
```

9. Add Remote Registry to GCS Bucket - Note change 'hisolver-data-collection-2' to you bucket name

```shell
dvc remote add -d processed_dataset gs://hisolver-data-collection-2/dvc_store
```

10. Add the dataset to registry and push

```shell
dvc add mushroom_dataset
dvc push
```

11. Update the git to track dvc locally

```shell
git add processed_data.dvc
git commit -m "tracking processed_data.dvc"
```
