import cv2

from ultralytics import YOLO


def run_inference():
    model = YOLO(path_model)
    results = model.predict(source=path_test_data, device=0, save=False, show_conf=False)
    return results


def extract_results(inf_results):
    image = cv2.imread(path_test_data)
    height, width = image.shape[:2]
    print(height, width)
    print(f"Height is {height} pixels and width is {width} pixels")
    print(f"Each box has a height of {round(height / 9 ,2)} pixels and a width of {round(width / 9 ,2)}")
    start = [[0 for j in range(9)] for i in range(9)]

    results = inf_results
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        center_x = x1 + 0.5 * (x2 - x1)
        center_y = y1 + 0.5 * (y2 - y1)
        name = names[int(cls)]
        row_idx = int(center_y // (height / 9))
        col_idx = int(center_x // (width / 9))
        print(f"x1 {x1:.2f}, x2 {x2:.2f}, y1 {y1:.2f}, y2 {y2:.2f}, center {center_x:.2f} {center_y:.2f}, name {name}, row idx {row_idx}, col idx {col_idx}")
        start[row_idx][col_idx] = int(name)
    print(start)


if __name__ == '__main__':
    path_test_data = ("D://OneDrive - Wageningen University & "
                      "Research//Documenten//Sudoku_project//Test_dataset//sudoku_1.png")
    path_model = "C://Users//johan//PycharmProjects//JustForFun//runs//detect//train//weights//best.pt"
    inference_results = run_inference()
    extract_results(inference_results)
