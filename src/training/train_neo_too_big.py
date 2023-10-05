import os
import json
from datetime import datetime

from google.cloud import storage
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPTNeoForCausalLM, GPT2Tokenizer, Trainer, TrainingArguments


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
        # Omit labeled/ when writing - so it's just dest_dir/file not dest_dir/labeled/file
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
    # Retieve labeled data, save locally to a data folder
    data_dir = '/app/data'
    preprocess_json(GCS_BUCKET_NAME, data_dir)
    print('===== Finished retrieving labeled data from bucket')

    # Load the data into PyTorch
    dataset = CustomDataset(data_dir)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Load pre-trained GPT-NEO 2.7B and tokenizer
    print('===== Loading model and tokenizer...')
    model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")
    tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")
    print('===== Finished loading model and tokenizer')

    # Define training arguments
    training_args = TrainingArguments(
        per_device_train_batch_size=32,
        output_dir='./results',
        num_train_epochs=1,  # You can adjust the number of epochs
        logging_dir='./logs',
        logging_steps=10,
    )

    # Define Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    # Train the model
    print('===== Fine-tuning...')
    trainer.train()
    print('===== Finished fine-tuning')

    # Save the trained model
    model_dir = '/app/fine-tuned'
    model.save_pretrained(model_dir)

    # ===== Demo =====
    print('===== Demo...')

    # Load the fine-tuned model
    model = GPTNeoForCausalLM.from_pretrained(model_dir)

    # Example demo to test the fine-tuned model
    prompt_text = "Create a function in Python to add two numbers"
    inputs = tokenizer(prompt_text, return_tensors="pt")
    outputs = model.generate(**inputs)
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f'Prompt: {prompt_text}')
    print('-----')
    print('Output:')
    print(generated_code)


if __name__ == '__main__':
    main()
