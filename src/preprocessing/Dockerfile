# Use a lightweight Python image
FROM python:3.9-slim

# Update the OS
RUN apt-get update && apt-get upgrade -y

# Install necessary dependencies for dask-distributed
RUN apt-get install -y gcc

# Install git
RUN apt-get install -y git

# Install required python packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install DVC with GCS support
# RUN pip install 'dvc[gcs]'

# Set working directory
WORKDIR /app

# Copy the preprocess script
COPY preprocessing.py /app/preprocessing.py

CMD ["python", "/app/preprocessing.py"]
