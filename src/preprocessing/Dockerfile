# Use a lightweight Python image
FROM python:3.9-slim

# Update the OS
RUN apt-get update && apt-get upgrade -y

# Install necessary packages for gcsfuse
RUN apt-get install -y wget gnupg lsb-release

# Install gcsfuse
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-buster main" > /etc/apt/sources.list.d/gcsfuse.list
RUN wget -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && apt-get install -y gcsfuse

# Install required python packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download the Punkt tokenizer data for NLTK
RUN python -m nltk.downloader punkt

# Set working directory
WORKDIR /app

# Copy the preprocess script
COPY preprocess.py /app/preprocess.py

CMD ["python", "/app/preprocess.py"]
