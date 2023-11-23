# HiSolver API

This repo uses Docker, FastAPI, and Python to create an API for managing and creating animations using language model-based search and question answering. It utilizes OpenAI's language model for document embeddings and ChromaDB for vector indexing and searching.

## Table of Contents
- [HiSolver API](#hisolver-api)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [API Usage](#api-usage)
  - [License](#license)

## Setup

To get started, clone this repository and navigate to the project directory.

First, copy the config_template.json and rename it to config.json. In the newly copied config.json file, add your API keys.

Now, you need to build and run a Docker container. Here are the commands you can use:

```bash
docker rm -f hisolver-MLOps-API
docker build -t hisolver-python3 .
docker run -d -v $(pwd):/hisolver-py -p 8001:8001 --restart always --name hisolver-MLOps-API hisolver-python3
```

The Docker commands above will build an image for the project, remove any existing container named `hisolver-pythonAPI`, and then run a new container with the project code mounted from your current directory. The application inside the container will listen on port 9000. 

## API Usage

This repo provides a FastAPI application with the following endpoints:

- `POST /animation_from_question`: This endpoint accepts a filename and query as parameters and creates a manim animation based on the query.
- more to come
  
You can access the API documentation and test the endpoints by navigating to `http://localhost:8001/docs` in your web browser.

## License

This project is open source under the MIT license. See [LICENSE](LICENSE) for details.

