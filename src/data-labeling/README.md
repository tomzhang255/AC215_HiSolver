# Data Labeling

## I. Check work

Make sure you've followed all the steps from the data pre-processing section `src/preprocessing/README.md`.

## II. Run data labeling docker contianers

1. Start a Docker daemon (i.e., open up Docker Desktop)

2. Copy the `secrets` folder from `src/preprocessing/secrets/` and paste it to `src/data-labeling/secrets`

3. Traverse to the correct directory: `src/data-labeling/`

4. Create an env file named `data-labeling.env` within the `secrets/` folder; make sure it lives here: `src/data-labeling/secrets/data-labeling.env`

5. Paste the following content into the env file, replacing the appropriate parts with real info. Note: GCP project name can be found on the GCP Console; your bucket name is in `secrets/gcs_bucket_name.txt`; you may use any username (but preferrably your harvard email) and password you'd like for Label Studio.

```shell
GCP_PROJECT=your_gcp_project_name
GCS_BUCKET_NAME=your_bucket_name
LABEL_STUDIO_USERNAME=your_harvard_email
LABEL_STUDIO_PASSWORD=any_password
```

6. Run containers:

```shell
# Create the network if we don't have it yet
docker network inspect hisolver-data-labeling-network >/dev/null 2>&1 || docker network create hisolver-data-labeling-network

# Build the image based on the Dockerfile
docker build -t hisolver-data-label-cli --platform=linux/arm64/v8 -f Dockerfile .

# Run All Containers
docker-compose run --rm --service-ports hisolver-data-label-cli
```

7. This should bring up a shell prompt from the running container

## III. Set up Label Studio

1. Go to this address using Google Chrome: http://localhost:8080/

2. It's essentially that you're using Google Chrome; Safari wouldn't rendering things properly!

3. Log in with the credentials you previously specified in the env file `secrets/data-labeling.env`

4. Create a project, give it a name: `HiSolver Manim Animation Labeling`

5. Skip `Data Import` tab and go to `Labeling Setup`

6. Select template: `Natural Language Processing` -> `Text Summarization`

7. Look for the tab with the two options `Code` and `Visual` and click on `Code`

8. Paste the following content in to specify the labeling interface UI:

```html
<View style="white-space: pre;">
  <header value="Review and/or run this piece of Manim code" />
  <Text name="text" value="$code" />
  <header value="Provide a one sentence summary of what it's rendering" />
  <textarea
    name="answer"
    toName="text"
    showSubmitButton="true"
    maxSubmissions="1"
    editable="true"
    required="true"
  />
</View>
```

9. Click `Save`

10. Make sure you're in the labeling project you just created, then click on `Settings`

11. Go to `Cloud Storage` -> `Add Source Storage`

12. Fill out the form:

- Storage Type: `Google Cloud Storage`
- Storage Title: `Manim Code Snippets`
- Bucket Name: `[your bucket name, look at secrets/gcs_bucket_name.txt]`
- Bucket Prefix: `processed`
- File Filter Regex: .\*
- Uncheck both marks (Treat every bucket object as a source file, Use pre-signed URLs)
- Do not touch Google Application Credentials and Google Project ID

13. Click `Add Storage`; click `Sync Storage` in the Source Cloud Storage section

14. Click `Add Target Storage`

15. Fill out the form:

- Storage Type: `Google Cloud Storage`
- Storage Title: `Manim Code Snippets`
- Bucket Name: `[your bucket name, look at secrets/gcs_bucket_name.txt]`
- Bucket Prefix: `labeled`

17. Click `Add Storage`; click `Sync Storage` in the Target Cloud Storage section

18. Enable cross-origin resource sharing (CORS) - In order to view images in Label studio directly from GCS Bucket, we need to enable CORS.

- Go to the shell where we ran the docker containers
- Run `python cli.py -c`

## IV. Use Label Studio to annotate Manim code snippets

1. Go to the home page of your labeling project

2. Select a task and complete it; the UI is really simple

3. In case your task list is not updating properly:

- From the home page of the labeling project, select all tasks with the top level check mark
- Click `Delete Tasks`
- Go to Settings for this labeling project -> `Cloud Storage`
- Click `Sync Storage` for both the source and target
