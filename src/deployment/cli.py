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
import json
import requests

from google.cloud import storage
from google.cloud import aiplatform
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer


GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
MODEL_NAME = 'best_model'
MODEL_DIR = f'models/{MODEL_NAME}'
ARTIFACT_URI = f"gs://{GCS_BUCKET_NAME}/{MODEL_DIR}"


def main(args=None):
    if args.upload:
        print("Upload model to GCS")

        model_name = 'distilgpt2'
        model = TFGPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)

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

        upload_model_to_gcs(MODEL_DIR, GCS_BUCKET_NAME, model_name)

        print(
            f'Model {model_name} has been uploaded to GCS bucket {GCS_BUCKET_NAME}.')

    elif args.deploy:
        print("Deploy model")

        def deploy_model(gcs_model_path, project, location='us-east4'):
            aiplatform.init(project=project, location=location)

            model = aiplatform.Model.upload(
                display_name='distilgpt2-tf',
                artifact_uri=gcs_model_path,
                serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-3:latest',
            )

            deployed_model = model.deploy(
                machine_type='n1-standard-4',
            )
            return deployed_model.endpoint

        endpoint = deploy_model(ARTIFACT_URI, GCP_PROJECT)
        print(f'Model deployed at: {endpoint}')

        response = endpoint.predict(data="Hello, world!")
        print(f'Response: {response}')

    elif args.predict:
        print("Predict using endpoint")

        # Assume endpoint is set up
        endpoint = "https://your-vertex-ai-endpoint-url"
        input_text = "Your input text here"

        def make_prediction(endpoint, input_text):
            # Prepare the request body
            request_body = {
                "instances": [{"input_text": input_text}]
            }

            # Send the prediction request
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(request_body)
            )

            # Check for a valid response
            if response.status_code == 200:
                # Parse the prediction results
                prediction_results = response.json()
                predictions = prediction_results.get("predictions", [])
                if predictions:
                    # Assume the first prediction is the most relevant
                    output_text = predictions[0]
                    return output_text
            else:
                print(
                    f"Failed to get a valid response. Status code: {response.status_code}")
                print(f"Response content: {response.content}")

            return None

        output_text = make_prediction(endpoint, input_text)
        if output_text:
            print(f"Output text: {output_text}")
        else:
            print("Failed to get a prediction")


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
