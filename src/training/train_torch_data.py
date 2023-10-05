import os
import json
from datetime import datetime

from google.cloud import storage
import torch
from torch.utils.data import Dataset, DataLoader


GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")


class CustomDataset(Dataset):
    def __init__(self, data_dir):
        self.data_files = [os.path.join(data_dir, f)
                           for f in os.listdir(data_dir)]
        self.data = []
        for file in self.data_files:
            with open(file, 'r') as f:
                data = json.load(f)
            self.data.append(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


def preprocess_json(bucket_name, dest_dir):
    gcs_client = storage.Client()
    bucket = gcs_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix='labeled/'))

    for blob in blobs:
        # omit labeled/ when writing - so it's just dest_dir/file not dest_dir/labeled/file
        file_path = f'/{dest_dir}/{blob.name[8:]}'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        blob.download_to_filename(file_path)
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extracting only the necessary fields then JSON to destination directory
        simplified_data = {'prompt': data['result'][0]['value']
                           ['text'][0], 'code': data['task']['data']['code']}
        with open(file_path, 'w') as f:
            json.dump(simplified_data, f)


def main():
    # retieve labeled data, save locally to a data folder
    data_dir = '/app/data'
    preprocess_json(GCS_BUCKET_NAME, data_dir)
    print('===== Finished retrieving labeled data from bucket')

    # Load the data into PyTorch
    dataset = CustomDataset(data_dir)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    for batch in dataloader:
        print(batch)  # FIXME Replace with your training code


if __name__ == '__main__':
    main()
