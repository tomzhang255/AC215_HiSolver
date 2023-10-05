# Use PyTorch base image
FROM pytorch/pytorch:latest

# Set the working directory
WORKDIR /app

# Copy training script
COPY train.py /app/train.py

# Install necessary libraries
RUN pip install --upgrade google-cloud-storage transformers transformers[torch]

# Set the entrypoint to run the script
ENTRYPOINT ["python", "train.py"]
