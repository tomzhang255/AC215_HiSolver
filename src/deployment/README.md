copy secrets from training folder

./run.sh

type Y at some point after container starts running

## serving pytorch model with pre-trained container to vertex ai

### Package the model artifacts in a model archive file

pip install torch-model-archiver

create mar/

```shell
torch-model-archiver -f \
    --model-name model \
    --version 1.0  \
    --serialized-file ./model.py \
    --handler custom_handler.py \
    --export-path mar/ \
    --extra-files extra/config.json,extra/tokenizer.json,extra/vocab.json,extra/generation_config.json,extra/generation_config_for_text_generation.json
```

### Copy the model artifacts to Cloud Storage

copy serice account email - in IAM page, add role "AI Platform Admin" to service account email principal
