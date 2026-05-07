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
  model=yolov8m.pt \
  data=../data/processed/parsed5.0/data.yaml \
  epochs=250 \
  imgsz=1280 \
  batch=8 \
  lr0=0.001 \
  warmup_epochs=5 \
  optimizer=SGD \
  patience=0 \
  project=../models/finetuned \
  name=yolov8m_baseline_finetuned_m \
  exist_ok=True \
  save_period=10