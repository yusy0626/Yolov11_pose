from ultralytics import YOLO


model = YOLO('yolov8n-pose.pt')  # load a pretrained model (recommended for training)

model.train(data='config.yaml', epochs=50, imgsz=640)
