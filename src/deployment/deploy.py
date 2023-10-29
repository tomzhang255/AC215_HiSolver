"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py --upload
        python cli.py --deploy
        python cli.py --predict
"""

import os
import argparse

from google.cloud import storage, aiplatform


def download_directory(bucket_name, source_dir_prefix):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=source_dir_prefix)
    for blob in blobs:
        destination_file_name = blob.name
        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
        blob.download_to_filename(destination_file_name)
        print(f'Downloaded {blob.name} to {destination_file_name}')


def main(args=None):
    # transformers = "*"
    # torch = "*"
    # torch-model-archiver = "*"

    # these make the image too big for pipeline, so installing them here
    os.system('pip install transformers torch torch-model-archiver')

    # Constants
    GCP_PROJECT = os.environ.get("GCP_PROJECT")
    if args.project != "":
        GCP_PROJECT = args.project

    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    if args.bucket != "":
        GCS_BUCKET_NAME = args.bucket

    MODEL_NAME = 'pytorch_model'
    MODEL_URI = f"gs://{GCS_BUCKET_NAME}/{MODEL_NAME}"
    REGION = 'us-east4'

    # ============================================================
    # upload
    # ============================================================

    print("Upload model archive to GCS")

    # download a pre-trained model
    model_path = "fine_tuned_model"  # where to locally store the download
    os.system(f'rm -r {model_path}')
    os.system(f'mkdir {model_path}')
    download_directory(GCS_BUCKET_NAME, 'fine_tuned_model/')

    # rename model bin
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
                    --extra-files {model_path}/config.json,{model_path}/vocab.json,{model_path}/generation_config.json \
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

    # remove local model
    os.system(f'rm -rf {model_path}')

    # ============================================================
    # deploy
    # ============================================================

    print('Deploy model to Vertex AI')

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


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Model Deployment CLI")

    parser.add_argument(
        "-b",
        "--bucket",
        type=str,
        default="",
        help="GCS bucket name",
    )

    parser.add_argument(
        "-prj",
        "--project",
        type=str,
        default="",
        help="GCP project name",
    )

    args = parser.parse_args()

    main(args)
