import os
import re
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
from google.cloud import storage


GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
MAX_FILES = 20  # The maximum number of files allowed in a folder.


def get_python_files_from_gcs(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    # get all raw files
    blobs = list(bucket.list_blobs(prefix='raw/'))  # Convert iterator to list here

    python_files = []
    dir_counts = defaultdict(int)

    for blob in blobs:
        dir_name = '/'.join(blob.name.split('/')[:-1])
        dir_counts[dir_name] += 1

    for blob in blobs:
        if blob.name.endswith('.py'):
            dir_name = '/'.join(blob.name.split('/')[:-1])
            if dir_counts[dir_name] <= MAX_FILES:
                python_files.append(blob)
            else:
                print(
                    f"Ignoring files in directory {dir_name} as it contains more than {MAX_FILES} files.")

    return python_files


def extract_pairs(content):
    pairs = re.findall(r'(#.*\n)([^\#]*)', content)
    return pairs


def clean_code(code):
    code = re.sub(r'#.*', '', code)
    code = code.replace('\t', '    ')
    return code.strip()


def tokenize(text):
    return word_tokenize(text)


def save_to_gcs(processed_content, file_path, bucket_name):
    file_name = f"processed/{file_path}.json"  # append a json at the end - cause the processed files will be in JSON format
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = storage.Blob(file_name, bucket)
    blob.upload_from_string(processed_content, content_type='text/plain')
    print(f"Saved to {file_name}")


def process_files(bucket_name):
    print(f"Processing files in bucket {bucket_name}...")
    python_files = get_python_files_from_gcs(bucket_name)

    for blob in python_files:
        print(f"Processing file: {blob.name}")
        content = blob.download_as_text()
        pairs = extract_pairs(content)
        processed_pairs = []

        for comment, code in pairs:
            code = clean_code(code)
            if comment and code:
                processed_pairs.append({
                    'input': ' '.join(tokenize(comment)),
                    'output': ' '.join(tokenize(code))
                })

        if processed_pairs:
            processed_content = json.dumps(processed_pairs, indent=4)
            save_to_gcs(processed_content, blob.name, bucket_name)


if __name__ == "__main__":
    process_files(GCS_BUCKET_NAME)
