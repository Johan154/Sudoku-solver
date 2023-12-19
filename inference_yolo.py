from ultralytics import YOLO


if __name__ == '__main__':
    path_test_data = "D://OneDrive - Wageningen University & Research//Documenten//Sudoku_project//Test_dataset"
    path_model = "C://Users//johan//PycharmProjects//JustForFun//runs//detect//train//weights//best.pt"
    model = YOLO(path_model)
    results = model.predict(source=path_test_data, device=0, save=True, show_conf=False)
    print(results)
