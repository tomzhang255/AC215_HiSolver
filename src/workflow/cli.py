"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip


GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
GCP_REGION = os.environ["GCP_REGION"]
DOCKER_HUB_USERNAME = os.environ['DOCKER_HUB_USERNAME']

# DATA_COLLECTOR_IMAGE = "gcr.io/ac215-project/mushroom-app-data-collector"
DATA_COLLECTOR_IMAGE = f"{DOCKER_HUB_USERNAME}/hisolver-manim-data-collector"
DATA_PROCESSOR_IMAGE = f"{DOCKER_HUB_USERNAME}/hisolver-manim-data-processor"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main(args=None):
    print("CLI Arguments:", args)

    if args.pipeline1:
        # Define a Container Component for data collector
        @dsl.container_component
        def data_collector():
            container_spec = dsl.ContainerSpec(
                image=DATA_COLLECTOR_IMAGE,
                command=[],
                args=[
                    "collect.py"
                ],
            )
            return container_spec

        # Define a Container Component for data processor
        @dsl.container_component
        def data_processor():
            container_spec = dsl.ContainerSpec(
                image=DATA_PROCESSOR_IMAGE,
                command=[],
                args=[
                    "preprocess.py"
                ],
            )
            return container_spec

        # Define a Pipeline
        @dsl.pipeline
        def ml_pipeline():
            # Data Collector
            data_collector_task = data_collector().set_display_name("Data Collector")
            # Data Processor
            data_processor_task = (
                data_processor()
                .set_display_name("Data Processor")
                .after(data_collector_task)
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(ml_pipeline, package_path="pipeline1.yaml")

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "hisolver-manim-pipeline-data-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="pipeline1.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-p1",
        "--pipeline1",
        action="store_true",
        help="HiSolver Manim Pipeline - Data",
    )
    parser.add_argument(
        "-p2",
        "--pipeline2",
        action="store_true",
        help="HiSolver Manim Pipeline - Model",
    )

    args = parser.parse_args()

    main(args)
