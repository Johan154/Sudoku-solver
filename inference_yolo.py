import os
import cv2

from ultralytics import YOLO


def run_inference():
    model = YOLO(path_model)
    class_labels = model.names
    results = model.predict(source=path_test_data, device=0, save=False, show_conf=False)
    return class_labels, results


def extract_results(class_labels, inf_results):
    image = cv2.imread(path_test_data)
    height, width = image.shape[:2]
    print(height, width)
    print(f"Height is {height} pixels and width is {width} pixels")
    print(f"Each box has a height of {round(height /9 ,2)} pixels and a width of {round(width /9 ,2)}")
    print(class_labels)
    boxes = inf_results[0].boxes.data
    for box in boxes:
        print(box)


if __name__ == '__main__':
    path_test_data = ("D://OneDrive - Wageningen University & "
                      "Research//Documenten//Sudoku_project//Test_dataset//sudoku_1.png")
    path_model = "C://Users//johan//PycharmProjects//JustForFun//runs//detect//train//weights//best.pt"
    labels, inference_results = run_inference()
    extract_results(labels, inference_results)
