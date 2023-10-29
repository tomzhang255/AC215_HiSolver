# Login to the hub:
docker login -u $(cat ../../secrets/docker_hub_username.txt) -p $(cat ../../secrets/docker_hub_token.txt)

# Build and tag the image:
docker build -t $(cat ../../secrets/docker_hub_username.txt)/hisolver-manim-model-trainer --platform=linux/amd64/v2 -f Dockerfile .

# Push to docker hub:
docker push $(cat ../../secrets/docker_hub_username.txt)/hisolver-manim-model-trainer
