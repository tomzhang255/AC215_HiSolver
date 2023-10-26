import os
import base64
import json
import requests
from time import sleep
import argparse

from google.cloud import storage


# Constants
GITHUB_API_URL = "https://api.github.com/search/repositories?q=manim"
PER_PAGE = 100


def get_python_files_from_repo(full_name, headers):
    """
    returns a list of tuples [(url, path), (url, path), ...]
    where url is where the content of the file lives on the github server (a blob)
    and the path is the actual path relative to the repo
    """

    repo_url = f"https://api.github.com/repos/{full_name}/git/trees/master?recursive=1"
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 404:
        repo_url = f"https://api.github.com/repos/{full_name}/git/trees/main?recursive=1"
        response = requests.get(repo_url, headers=headers)
        if response.status_code == 404:
            return []

    tree = response.json()
    return [(item['url'], item['path']) for item in tree.get('tree', []) if item['path'].endswith('.py')]


def save_to_gcs(file_url, file_path, bucket_name, headers):
    # get file content
    response = requests.get(file_url, headers=headers)
    if response.status_code != 200:
        return

    # decode
    res_data = json.loads(response.text)
    content = res_data.get('content')
    if content is None:
        return

    try:
        decoded_content = base64.b64decode(content).decode('utf-8')
    except UnicodeDecodeError:
        return

    # file name to upload to bucket
    parts = file_url.split("/")
    # store everything in the raw/ folder
    # -5 is account name, -4 is repo name
    file_name = f"raw/{parts[-5]}/{parts[-4]}/{file_path}"

    # upload to bucket
    blob = storage.Blob(file_name, storage.Client().get_bucket(bucket_name))
    blob.upload_from_string(decoded_content, content_type='text/plain')

    print(file_name)


def main(args=None):
    """
    Using a pagination loop to collect all API requests
    because each API response only gives max 100 items.
    """
    # constants

    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    # If bucket was passed as argument
    if args.bucket != "":
        GCS_BUCKET_NAME = args.bucket

    GITHUB_TOKEN = os.environ.get("GITHUB_PAT")
    if args.pat != "":
        GITHUB_TOKEN = args.pat

    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    page = 1
    repos = 0

    # simple API call pagination mechanism
    while True:
        # get a list of 100 repos containing keyword "manim"
        response = requests.get(
            f"{GITHUB_API_URL}&per_page={PER_PAGE}&page={page}", headers=HEADERS)
        try:
            response.raise_for_status()
        except:
            print(f'Failed to /GET page {page}; skipping...')
            print(f"{GITHUB_API_URL}&per_page={PER_PAGE}&page={page}",
                  headers=HEADERS)
            print(response.text)
            continue

        items = response.json().get('items', [])

        if not items:
            break

        # each item is a repo
        for item in items:
            # for each repo, get all python files
            python_files = get_python_files_from_repo(
                item['full_name'], HEADERS)
            sleep(1)
            for file_url, file_path in python_files:
                # save each python file to GCP bucket
                save_to_gcs(file_url, file_path, GCS_BUCKET_NAME, HEADERS)

            # FIXME for now just collect 5 repos for testing purposes
            repos += 1
            if repos == 5:
                return

        print(f"--- Page: {page} done ---")
        page += 1

    print('--- All pages done ---')


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Collector CLI")

    parser.add_argument(
        "-b",
        "--bucket",
        type=str,
        default="",
        help="GCS bucket name",
    )
    parser.add_argument(
        "-p",
        "--pat",
        type=str,
        default="",
        help="GitHub PAT",
    )

    args = parser.parse_args()

    main(args)
