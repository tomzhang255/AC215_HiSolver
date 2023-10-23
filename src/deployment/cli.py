"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py --upload
        python cli.py --deploy
        python cli.py --predict
"""

import os
import argparse
import glob
import base64
import json
import pathlib
import urllib.request

from google.cloud import storage, aiplatform
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch


GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
MODEL_NAME = 'best_model'
MODEL_DIR = f'models/{MODEL_NAME}'
ARTIFACT_URI = f"gs://{GCS_BUCKET_NAME}/{MODEL_DIR}"


def main(args=None):
    if args.upload:
        print("Upload model to GCS")

        model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')

        os.makedirs(MODEL_DIR, exist_ok=True)
        model.save_pretrained(MODEL_DIR)
        tokenizer.save_pretrained(MODEL_DIR)

        def upload_model_to_gcs(local_model_dir, bucket_name, model_name):
            storage_client = storage.Client(project=GCP_PROJECT)
            bucket = storage_client.get_bucket(bucket_name)
            local_files = [f for f in glob.glob(
                f"{local_model_dir}/**", recursive=True) if os.path.isfile(f)]
            for local_file in local_files:
                remote_path = os.path.join(
                    model_name, os.path.relpath(local_file, local_model_dir))
                blob = bucket.blob(remote_path)
                blob.upload_from_filename(local_file)

        upload_model_to_gcs(MODEL_DIR, GCS_BUCKET_NAME, MODEL_NAME)

        print(
            f'Model {MODEL_NAME} has been uploaded to GCS bucket {GCS_BUCKET_NAME}.')

    elif args.deploy:
        # init vertex ai sdk
        # aiplatform.init(project=GCP_PROJECT, location='us-east4', staging_bucket=f'gs://{GCS_BUCKET_NAME}')

        # Create a TorchServe inference handler.
        def handler(data):
            # Process the input data.
            tokenizer = GPT2Tokenizer.from_pretrained(ARTIFACT_URI)
            input_ids = tokenizer.encode(data)

            # Run the model inference.
            model = GPT2LMHeadModel.from_pretrained(ARTIFACT_URI)
            outputs = model(input_ids=torch.tensor(input_ids))
            generated_ids = outputs.logits.argmax(dim=-1)

            # Post-process the output data.
            output = tokenizer.decode(generated_ids.tolist())

            return output

        # Create a TorchServe model config.
        model_config = torchserve.ModelConfig(
            name=MODEL_NAME,
            handler=handler,
            model_path=ARTIFACT_URI,
            runtime="pytorch",
        )


        # us-docker.pkg.dev/vertex-ai/prediction/pytorch-cpu.2-0:latest




        # Create a Vertex AI Model resource.
        aiplatform.init()
        model = aiplatform.Model.create(
            project_id=GCP_PROJECT,
            region="us-east4",
            display_name=MODEL_NAME,
            framework="pytorch",
            model_config=model_config,
        )

        # Deploy the model to a Vertex AI endpoint.
        endpoint = model.deploy(endpoint_name=f"{MODEL_NAME}-endpoint")

        print(endpoint)

        # Send a prediction request to the endpoint.
        response = endpoint.predict(data="Hello, world!")

        # Print the prediction response.
        print(response)

    elif args.predict:
        print("Predict using endpoint")


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Model Deployment CLI")

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload saved model to GCS Bucket",
    )
    parser.add_argument(
        "-d",
        "--deploy",
        action="store_true",
        help="Deploy saved model to Vertex AI",
    )
    parser.add_argument(
        "-p",
        "--predict",
        action="store_true",
        help="Make prediction using the endpoint from Vertex AI",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Test deployment to Vertex AI",
    )

    args = parser.parse_args()

    main(args)
