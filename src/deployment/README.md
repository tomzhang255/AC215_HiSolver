## serving pytorch model with pre-trained container to vertex ai

in gcp console: copy serice account email - in IAM page, add role "AI Platform Admin" to service account email principal

be in the deployment/ dir, to build and run a docker container, a shell will be launch at the end:

```shell
./docker-shell.sh
```

in the docker shell:

```shell
python cli.py --upload
```

```shell
python cli.py --deploy
```
