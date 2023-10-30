# Use PyTorch base image
FROM pytorch/pytorch:latest

# Set the working directory
WORKDIR /app

# Copy training script
COPY train.py /app/train.py

# Copy service account key
COPY secrets/data-service-account.json /secrets/data-serivce-account.json
COPY secrets/gcs_bucket_name.txt /secrets/gcs_bucket_name.txt

# Copy docker entrypoint
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Install necessary libraries
RUN pip install --upgrade google-cloud-storage torch transformers transformers[torch]

# Use shell to read the GCS bucket name from file and set it as an environment variable
RUN echo "export GCS_BUCKET_NAME=$(cat /secrets/gcs_bucket_name.txt)" >> /etc/environment

# Set the Google Application Credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-serivce-account.json

RUN pip install -r requirements.txt

# Set the entrypoint to run the script
ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]
