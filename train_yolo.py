from ultralytics import YOLO


if __name__ == '__main__':
    path_train_data = "D://OneDrive - Wageningen University & Research//Documenten//Sudoku_project//Train_dataset//YOLODataset//dataset.yaml"
    model = YOLO('yolov8n.pt')
    results = model.train(data=path_train_data, epochs=300, imgsz=1280, device=0)
