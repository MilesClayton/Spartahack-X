import modal
from ultralytics import YOLO
import torch
import os
vol = modal.Volume.from_name("my-volume")

app = modal.App("something")
datascience_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("libgl1-mesa-glx")
    .apt_install("libglib2.0-0")
    .pip_install( "numpy", "ultralytics", "opencv-python", "torch", "torchvision")
    .add_local_dir("test", remote_path="/root/test")
    .add_local_dir("train", remote_path="/root/train")
    .add_local_dir("valid", remote_path="/root/valid")
    .add_local_file("/yolov8n.pt", remote_path="/root/yolov8n.pt")
    .add_local_file("data.yaml", remote_path="/root/data.yaml")

)

@app.function(gpu="any", image=datascience_image, volumes={"/data": vol}, timeout=14400)
def my_function():
    model = YOLO('/root/yolov8n.pt')  # Load pretrained model
    results = model.train(
        data='/root/data.yaml',  # Path to your YAML config file
        epochs=75,  # Number of training epochs
        batch=8,  # Batch size
        imgsz=640,  # Image size
        name='my_model',  # Name for the trained model
        device=0,
    )
    model.save('/data/model.pt')
    # os.system("yolo train model=/root/yolov8n.pt data=/root/data.yaml epochs=10 imgsz=640 device=gpu")

@app.local_entrypoint()
def new_funct():
    my_function.remote()

