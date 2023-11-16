# Model Deployment

## I. Check work

Make sure you've followed all the steps from the data pre-processing section `src/training/README.md`.

## II. Grant service account permissions

1. Go to GCP console, use either the sidebar navigation menu or search bar to navigate to `IAM & Admin`-> `Service Accounts`

2. Copy the email of the service account you've been using; it should look something like `[service-account-name]@[project-name].iam.gserviceaccount.com`

3. Navigate to `IAM & Admin` -> `IAM`

4. Click on `GRANT ACCESS`; paste your service account email into the `New principals` field; select the role of `AI Platform Admin`; just in case, add another role of `Vertex AI Admin` too

## III. Build and test-run docker container

1. In your terminal, navigate to `src/deployment/`

2. Execute this script to build and run a docker container; a shell prompt will be launched at the end:

```shell
./docker-shell.sh
```

3. In the container's shell:

```shell
python deploy.py
```

4. Once the script finishes running, you can safely quit the container's shell

## IV. Push the image you just built to docker hub

1. Run this:

```shell
./docker-hub.sh
```
