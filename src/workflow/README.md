## prep

make sure you've followed all the steps from the previous sections; in particular, images must be pushed to docker hub.

in secrets folder: add - gcs_service_account.txt

on gcp console - add service account as "service account user"

## note

because label studio requires setting things up with its UI manually, it cannot be automated as part of the pipeline; hence, we're breaking the pipeline into two parts.

pipeline 1: data collection -> data preprocessing
human intervention: set up label studio separately and populate bucket with annotated data
pipeline 2: model training -> model deployment

## run pipeline on vertex ai

```shell
./docker-shell.sh
```

```shell
python cli.py --pipeline1
```

once you see "PipelineState.PIPELINE_STATE_RUNNING" that means the pipeline has been deployed and is running; you can safely quit the docker shell and check on gcp console (select the right region: us-east4)

wait til the pipeline finishes, then do label studio stuff... then:

```shell
python cli.py --pipeline2
```
