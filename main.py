def check_cross():
    return 0


def check_items(in_sud):
    for row in in_sud:
        for sub_row in row:
            for i in sub_row:
                if i > 0:
                    print(i, in_sud.index(row))
    return 0


if __name__ == '__main__':
    start = \
        [[[5, 3, 0], [0, 7, 0], [0, 0, 0]],
         [[6, 0, 0], [1, 9, 5], [0, 0, 0]],
         [[0, 9, 8], [0, 0, 0], [0, 6, 0]],
         [[8, 0, 0], [0, 6, 0], [0, 0, 3]],
         [[4, 0, 0], [8, 0, 3], [0, 0, 1]],
         [[7, 0, 0], [0, 2, 0], [0, 0, 6]],
         [[0, 6, 0], [0, 0, 0], [2, 8, 0]],
         [[0, 0, 0], [4, 1, 9], [0, 0, 5]],
         [[0, 0, 0], [0, 8, 0], [0, 7, 9]]]
    check_items(start)
