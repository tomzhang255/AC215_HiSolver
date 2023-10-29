# Workflow Automation

## I. Check work

Make sure you've followed all the steps from each of the individual steps of the data pipeline:

- Data collection: `src/collection/README.md`
- Data pre-processing: `src/preprocessing/README.md`
- Data versioning: `src/data-versioning/README.md`
- Data labeling: `src/data-labeling/README.md`
- Model training: `src/training/README.md`
- Model deployment: `src/deployment/README.md`

In particular, pay special attention to the last steps of collection, preprocessing, and deployment - where push to docker hub is required; as we will be using their images in our Vertex AI Pipeline.

## II. Prep secrets and service account permissions

1. On GCP console, navigate to `IAM & Admin` -> `Service Accounts`; copy the email of the service account you've been using; it should look something like `[service-account-name]@[project-name].iam.gserviceaccount.com`

2. Create a new secret file named `gcs_service_account.txt` and paste the service account email into it; make sure this file resides in the `secrets/` folder

3. On GCP console, navigate to `IAM & Admin` -> `IAM`; click on `GRANT ACCESS`; paste your service account email into the `New principals` field; select the role of `Service Account User` (as we'll be using this service account to run pipeline jobs)

## III. Run pipeline on Vertex AI

1. Build and run docker container:

```shell
./docker-shell.sh
```

2. In the container's shell, execute pipeline (part 1):

```shell
python cli.py --pipeline1
```

3. Once you see `PipelineState.PIPELINE_STATE_RUNNING` from the python script's output - that means the pipeline has been deployed and is running; you can terminate the python script with `ctrl+c`; but do not quit the docker container's shell yet

4. To inspect the pipeline's progress:

   - navigate to `Vertex AI` -> `Pipelines` on GCP console;
   - Under the `RUNS` tab, select the right region (`us-east4`)
   - You should be able to see a list of all the pipelines you have
   - Click on the one you just deployed to see its progress

5. Wait til the pipeline finishes running (it should take less than 15 minutes); note that the first pipeline we just run is for data collection and preprocessing only; the second pipeline will be run after we've labeled some data

6. In the terminal, navigate to `src/data-labeling/`; follow the instructions in `README.md` to label some data

7. Navigate back to `src/workflow/`; the docker container's shell should still be running; if not, run `./docker-shell.sh` again

8. In the container's shell, execute pipeline (part 2):

```shell
python cli.py --pipeline2
```

9. Again, once you see `PipelineState.PIPELINE_STATE_RUNNING` - that means the pipeline has been deployed and is running; you can safely terminate the python script and quit the docker shell this time

10. Check the pipeline's progress on GCP console; it should take less than 20 minutes to finish
