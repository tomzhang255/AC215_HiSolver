docker rm -f hisolver-MLOps-API
docker build -t hisolver-python3 .
docker run -d -v $(pwd):/hisolver-py -p 8001:8001 --restart always --name hisolver-MLOps-API hisolver-python3
