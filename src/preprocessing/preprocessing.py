import os
import ast
import astor
import json
import tempfile
from datetime import datetime
import shutil
import sys
import subprocess
import dask
from dask import delayed
from dask.distributed import Client
from google.cloud import storage

DVC_REMOTE_NAME = os.environ.get("DVC_REMOTE_NAME")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
os.environ["HOME"] = "/app"


def extract_classes(temp_dir, blob_name):
    """
    returns a tuple: (a list of class definition code blocks, then the python file name)
    """
    # Read the file
    file_path = os.path.join(temp_dir, blob_name)
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # Parse the file
    try:
        tree = ast.parse(file_contents)
    except SyntaxError as e:
        # print(f"Failed to parse {blob_name}: {e}")
        return [], blob_name

    # Extract class definitions
    class_defs = [
        astor.to_source(node) for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    # print(f'Extracted classes from {blob_name}')

    return class_defs, blob_name


if __name__ == '__main__':
    t0 = datetime.now()

    client = Client()  # Initialize a Dask client
    gcs_client = storage.Client()
    bucket = gcs_client.get_bucket(GCS_BUCKET_NAME)

    # Download the Python files to a temporary directory
    temp_dir = tempfile.mkdtemp()
    blobs = list(bucket.list_blobs(prefix='raw/'))
    for blob in blobs:
        file_path = os.path.join(temp_dir, blob.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        blob.download_to_filename(file_path)

    print('===== Finished downloading files from GSC')
    sys.stdout.flush()

    # Use Dask to process the files in parallel
    delayed_tasks = [delayed(extract_classes)(temp_dir, blob.name)
                     for blob in blobs]
    results = dask.compute(*delayed_tasks)

    print('===== Finished processing with Dask')
    sys.stdout.flush()

    # Save the results to GCS
    processed_dir = 'processed'
    for class_def_list, python_file_name in results:
        for idx, class_def in enumerate(class_def_list):
            # note each class_def_list is associated with a python file
            # we want to separate each class definition snippet into its own file
            # so we generate a file name by appending index to original python file name
            json_filename = f'{processed_dir}/{python_file_name[4:]}-{idx}.json'
            os.makedirs(os.path.dirname(json_filename), exist_ok=True)
            with open(json_filename, 'w') as f:
                # this is the data format required for Lebel Studio
                json.dump({"data": {"code": class_def}}, f)
            # Upload the JSON file to GCS
            blob = bucket.blob(json_filename)
            blob.upload_from_filename(json_filename)

    print('===== Finished saving results to GCS')
    sys.stdout.flush()

    # DVC operations
    os.chdir('/app')  # Ensure we're in the right directory
    subprocess.run(["dvc", "add", processed_dir])  # Track processed directory with DVC
    subprocess.run(["dvc", "push", "-r",DVC_REMOTE_NAME])  # Push changes to DVC remote on GCS
    subprocess.run(["git", "add", ".dvc", f"{processed_dir}.dvc"])  # Add DVC metadata files to Git
    subprocess.run(["git", "commit", "-m", "Update processed data"])  # Commit the DVC changes to Git

    # Optionally, clean up the temporary directory
    shutil.rmtree(temp_dir)
    shutil.rmtree(processed_dir)

    t1 = datetime.now()
    print(f'===== Time elasposed to pre-process: {t1 - t0}')
    sys.stdout.flush()
