# Use PyTorch base image
FROM pytorch/pytorch:latest

# Set the working directory
WORKDIR /app

# Copy training script
COPY train.py /app/train.py

# Copy service account key
COPY secrets/data-service-account.json /secrets/data-serivce-account.json
COPY secrets/gcs_bucket_name.txt /secrets/gcs_bucket_name.txt

# Install necessary libraries
RUN pip install --upgrade google-cloud-storage torch transformers transformers[torch]

# Use shell to read the GCS bucket name from file and set it as an environment variable
RUN echo "export GCS_BUCKET_NAME=$(cat /secrets/gcs_bucket_name.txt)" >> /etc/environment

# Set the Google Application Credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-serivce-account.json

# Set the entrypoint to run the script
# ENTRYPOINT ["python", "train.py", "--bucket ($cat /secrets/gcs_bucket_name.txt)"]
ENTRYPOINT python train.py --bucket $(cat /secrets/gcs_bucket_name.txt)
