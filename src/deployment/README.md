## serving pytorch model with pre-trained container to vertex ai

copy secrets from training folder

in gcp console: copy serice account email - in IAM page, add role "AI Platform Admin" to service account email principal

be in the deployment/ dir, to build and run a docker container, a shell will be launch at the end:

```shell
./run.sh
```

in the docker shell:

```shell
python cli.py --upload
```

```shell
python cli.py --deploy
```
