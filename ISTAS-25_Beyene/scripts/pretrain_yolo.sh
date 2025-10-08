#!/bin/bash

MODEL="yolov10m.yaml"
PROJECT_NAME="pretrain_bda"
RUN_NAME="yolov10m_synthetic"
EPOCHS=200
IMGSZ=1280
BATCH=8                
DEVICE=0
DATA_YAML="synthetic_dataset_kde_final2/data.yaml"

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

if ! command -v yolo &> /dev/null
then
    echo "Ultralytics not installed. Installing..."
    pip install -U ultralytics
fi

echo "Running on device(s): $DEVICE"
nvidia-smi

yolo task=detect \
  mode=train \
  model=$MODEL \
  data=$DATA_YAML \
  epochs=$EPOCHS \
  imgsz=$IMGSZ \
  batch=$BATCH \
  device=$DEVICE \
  optimizer=SGD \
  weight_decay=0.01 \
  cos_lr=True \
  warmup_epochs=3 \
  lr0=0.001 \
  amp=True \
  seed=42 \
  save=True \
  save_period=10 \
  project=$PROJECT_NAME \
  name=$RUN_NAME \
  exist_ok=True
