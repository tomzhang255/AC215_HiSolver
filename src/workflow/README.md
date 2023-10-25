## prep

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

do label studio stuff... then:

```shell
python cli.py --pipeline2
```
