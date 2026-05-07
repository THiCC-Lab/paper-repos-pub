#!/bin/bash

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
  model=../models/pretrained/pretrain_bda/yolov10m_synthetic/weights/best.pt \
  data=../data/processed/parsed5.0/data.yaml \
  epochs=250 \
  imgsz=1280 \
  lr0=0.001 \
  device=0 \
  batch=8 \
  project=finetune_doclayout \
  name=yolov10m_pretrained_pm \
  exist_ok=True \
  warmup_epochs=5 \
  optimizer=SGD \
  patience=0 \
  exist_ok=True \
  save_period=10