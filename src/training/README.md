# LLM Fine-tuning

## I. Check work

Make sure you've followed all the steps from the data pre-processing section `src/data-labeling/README.md`.

## II. Training-related setup

1. Copy the `secrets/` folder from `src/secrets/` so it now has a copy at `src/training/secrets/`

## III. Serverless training with Vertex AI

1. Go to Google Cloud Platform Console -> select your project -> search for "Vertex AI" in the search bar -> Click "ENABLE ALL RECOMMENDED APIS" on the home page

2. Still on the console -> search for "Container Registry" in the search bar -> make sure the Container Registry API is enabled

3. Install Google Cloud SDK on your local machine (https://cloud.google.com/sdk/docs/install)

4. In `src/training/secrets/` create a file named `gcp_project_id.txt` and put the GCP Project ID that you've been using in it

5. Submit custom job to Vertex AI for serverless training:

```shell
./serverless.sh
```

6. To monitor training status:

- On the GCP console -> search for "Vertex AI" with the search bar
- On the Vertex AI page -> look at the sidebar -> look for the "MODEL DEVELOPMENT" section -> select "Training"
- On the Training page -> select region "us-east4" as we previously specified in the above command
- Go to the "CUSTOM JOBS" tab
- You should then see your job named: "hisolver-manim-training-job"
- After the job is done running, you should see a new folder `fine_tuned_model` in your GCS bucket
