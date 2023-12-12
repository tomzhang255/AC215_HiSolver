#!/bin/bash

set -e

export IMAGE_NAME="hisolver-manim-app-frontend-react-test"

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -p 8080:80 $IMAGE_NAME
