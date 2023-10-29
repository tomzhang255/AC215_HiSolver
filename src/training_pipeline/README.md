# LLM Fine-tuning

## I. Note

This directory will contribute to the final Vertex AI pipeline.

## II. Build and run docker container

1. Build and run container; a shell prompt will be launched:

```shell
./docker-shell.sh
```

2. Test-run the training script:

```shell
python train.py
```

## II. Push image to docker hub

1. Run this script to push image to docker hub:

```shell
./docker-hub.sh
```
