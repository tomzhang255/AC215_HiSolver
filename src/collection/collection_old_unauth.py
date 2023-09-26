import requests
from google.cloud import storage


GITHUB_API_URL = "https://api.github.com/search/repositories?q=manim"
GCS_BUCKET_NAME = "hisolver-data-collection"


def get_python_files_from_repo(full_name):
    repo_url = f"https://api.github.com/repos/{full_name}/git/trees/master?recursive=1"
    response = requests.get(repo_url)
    response.raise_for_status()

    tree = response.json()
    return [item['url'] for item in tree.get('tree', []) if item['path'].endswith('.py')]


def save_to_gcs(file_url, bucket_name):
    response = requests.get(file_url)
    response.raise_for_status()

    file_name = file_url.split("/")[-1] + '.py'
    blob = storage.Blob(file_name, storage.Client().get_bucket(bucket_name))
    blob.upload_from_string(response.text, content_type='text/plain')


def main():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()

    items = response.json()['items']

    print(len(items))
    print(items)
    exit()

    for item in items:
        python_files = get_python_files_from_repo(item['full_name'])
        for file_url in python_files:
            save_to_gcs(file_url, GCS_BUCKET_NAME)


if __name__ == "__main__":
    main()
