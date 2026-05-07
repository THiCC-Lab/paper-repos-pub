#!/bin/bash

SEEDS=(42 123 2024)
YOLO_MODEL="yolov8m.pt"
EPOCHS=200
BATCH=8
PROJECT_DIR="yolo_runs_random"
IMG_SIZE=1280

for SEED in "${SEEDS[@]}"
do
  SPLIT_DIR="splits/seed${SEED}"
  DATA_YAML="${SPLIT_DIR}/data.yaml"
  RUN_NAME="yolov8_random_seed${SEED}"

  # Efficient training with heavy augmentation and early stopping
  yolo train model=$YOLO_MODEL data=$DATA_YAML epochs=$EPOCHS batch=$BATCH project=$PROJECT_DIR name=$RUN_NAME seed=$SEED imgsz=$IMG_SIZE --optimizer=AdamW --patience=25 --device=0  

  # Validation (best checkpoint)
  yolo val model="$PROJECT_DIR/$RUN_NAME/weights/best.pt" data=$DATA_YAML project=$PROJECT_DIR name="val${RUN_NAME}" imgsz=$IMG_SIZE --device=0 
done