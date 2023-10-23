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
MODEL_NAME = 'pytorch_model'
MODEL_URI = f"gs://{GCS_BUCKET_NAME}/{MODEL_NAME}"
REGION = 'us-east4'


def main(args=None):
    if args.upload:
        print("Upload model to GCS")

        # download a pre-trained model
        model_path = "model"  # where to locally store the download
        os.system(f'rm -r {model_path}')
        os.system(f'mkdir {model_path}')

        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        model = GPT2LMHeadModel.from_pretrained('distilgpt2')

        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)

        os.system(
            f'mv {model_path}/pytorch_model.bin {model_path}/{MODEL_NAME}.bin')
        model_file = f"{model_path}/{MODEL_NAME}.bin"

        # Add torch-model-archiver to the PATH
        os.environ["PATH"] = f'{os.environ.get("PATH")}:~/.local/bin'

        # Package the model artifacts in a model archive file
        os.system(f"""
                    torch-model-archiver -f \
                        --model-name model \
                        --version 1.0  \
                        --serialized-file {model_file} \
                        --handler custom_handler.py \
                        --extra-files model/config.json,model/vocab.json,model/generation_config.json \
                        --export-path {model_path}
                    """)

        # Copy the model artifacts to Cloud Storage
        os.system(f"""
                    gsutil rm -r {MODEL_URI}
                    gsutil cp -r {model_path} {MODEL_URI}
                    gsutil ls -al {MODEL_URI}
                    """)

        print(
            f'Model {MODEL_NAME} has been uploaded to GCS bucket {GCS_BUCKET_NAME}.')

    elif args.deploy:
        # init vertex ai resource
        aiplatform.init(project=GCP_PROJECT, location=REGION,
                        staging_bucket=MODEL_URI)

        DEPLOY_IMAGE_URI = "us-docker.pkg.dev/vertex-ai/prediction/pytorch-cpu.1-11:latest"

        # upload model for deployment
        deployed_model = aiplatform.Model.upload(
            display_name=MODEL_NAME,
            serving_container_image_uri=DEPLOY_IMAGE_URI,
            artifact_uri=MODEL_URI,
        )

        # deploy model for prediction
        print('Deploying model...')
        print('This will take a few minutes...')

        DEPLOY_COMPUTE = "n1-standard-4"

        endpoint = deployed_model.deploy(
            deployed_model_display_name=MODEL_NAME,
            machine_type=DEPLOY_COMPUTE,
            accelerator_type=None,
            accelerator_count=0,
        )

        print('Model deployed!')
        print('Endpoint:')
        print(endpoint)

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
