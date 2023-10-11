# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables to ensure output is unbuffered and file I/O is set accordingly
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg apt-utils python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create symlink for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    DEBIAN_FRONTEND=noninteractive apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install google-cloud-sdk -y

# Set environment variable for the Google Cloud SDK to suppress telemetry
ENV CLOUDSDK_CORE_DISABLE_PROMPTS=1

# Copy the current directory content into the container at /app
COPY . /app/

# pip install
RUN pip install -r /app/requirements.txt

# Specify the command to run on container start
CMD [ "python", "./collection.py" ]
