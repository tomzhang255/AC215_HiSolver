import os
import json
import argparse
from datetime import datetime

from google.cloud import storage
from torch.utils.data import Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments


def preprocess_json(bucket_name, dest_file):
    gcs_client = storage.Client()
    bucket = gcs_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix='labeled/'))

    processed_data = []  # list to hold processed json objects

    for blob in blobs:
        # download blob content to a string
        blob_data = blob.download_as_text()
        data = json.loads(blob_data)

        # Extracting only the necessary fields
        simplified_data = {
            'prompt': data['result'][0]['value']['text'][0],
            'code': data['task']['data']['code']
        }

        processed_data.append(simplified_data)  # append processed data to list

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

    # Write all processed data to a single json file
    with open(dest_file, 'w') as f:
        json.dump(processed_data, f)


def upload_directory_to_gcs(bucket_name, source_directory_path, destination_directory_path):
    """Uploads a local directory to GCS"""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    for root, dirs, files in os.walk(source_directory_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            blob_destination_path = os.path.join(
                destination_directory_path, local_file_path[len(source_directory_path) + 1:])
            blob = bucket.blob(blob_destination_path)
            blob.upload_from_filename(local_file_path)
            print(f'{local_file_path} uploaded to {blob_destination_path}.')


class CustomDataset(Dataset):
    def __init__(self, filename, tokenizer):
        with open(filename, 'r') as f:
            self.data = json.load(f)
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        item = self.data[i]
        text = f"Prompt: {item['prompt']} Code: {item['code']}"
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',  # Pad to max_length
            max_length=128,  # You can adjust this value based on your needs
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'][0],
            'attention_mask': encoding['attention_mask'][0],
            # assuming language modeling objective
            'labels': encoding['input_ids'][0]
        }


def main(args=None):
    # contants
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    # If bucket was passed as argument
    if args.bucket != "":
        GCS_BUCKET_NAME = args.bucket

    # Retieve labeled data, save locally to a data folder
    data_file = '/app/data.json'
    preprocess_json(GCS_BUCKET_NAME, data_file)
    print('> Finished retrieving labeled data from bucket')

    # Load the distilled GPT-2 model and tokenizer
    model = GPT2LMHeadModel.from_pretrained("distilgpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

    # Add the [PAD] token to the tokenizer and model
    # GPT-2 uses the EOS token as the PAD token
    pad_token_id = tokenizer.eos_token_id
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = pad_token_id

    # Set the pad_token
    if tokenizer.pad_token is None:
        tokenizer.add_tokens(['[PAD]'])
        tokenizer.pad_token = '[PAD]'

    # Load the custom dataset
    train_dataset = CustomDataset(data_file, tokenizer)

    # Define the Trainer and TrainingArguments
    training_args = TrainingArguments(
        output_dir="./gpt2-qa",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=32,
        save_steps=10_000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    # Train the model
    t0 = datetime.now()
    trainer.train()
    t1 = datetime.now()
    print("> Training took: ", t1 - t0)

    # demo
    input_text = "say something"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=50,
                            num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f'> Q: {input_text}')
    print(f'> A: {decoded_output}')

    # save model and tokenizer

    model.save_pretrained('model')
    tokenizer.save_pretrained('model')

    # upload to bucket
    upload_directory_to_gcs(GCS_BUCKET_NAME, 'model', 'fine_tuned_model')

    # remove files
    os.system('rm -rf data.json')
    os.system('rm -rf gpt2-qa/')
    os.system('rm -rf model/')


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Trainer CLI")

    parser.add_argument(
        "-b",
        "--bucket",
        type=str,
        default="",
        help="GCS bucket name",
    )

    args = parser.parse_args()

    main(args)
