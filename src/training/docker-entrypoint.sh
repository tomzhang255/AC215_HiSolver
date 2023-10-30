#!/bin/bash

# To prep dataset and test-run fine-tuning without optimization
python train.py --bucket $(cat /secrets/gcs_bucket_name.txt)

# Apply QLoRA optimization
python qlora.py \
    --model_name_or_path ./model \
    --output_dir ./out \
    --dataset ./data \
    --dataset-format input-output \
    --train_on_source True \
    --learning_rate 0.000075 \
    --warmup_steps 0 \
    --num_train_epochs 1 \
    --do_train True \
    --do_eval True \
    --do_mmlu_eval False \
    --bf16 True \
    --bits 16 \
    --source_max_len 2500 \
    --target_max_len 2500 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 1 \
    --logging_first_step true --logging_steps 1 \
    --save_steps 100 \
    --eval_steps 10 \
    --save_strategy steps \
    --save_total_limit 2 \
    --data_seed 41 \
    --per_device_eval_batch_size 1 \
    --fp16_full_eval \
    --evaluation_strategy steps \
    --max_memory_MB 48000 \
    --optim paged_adamw_32bit
