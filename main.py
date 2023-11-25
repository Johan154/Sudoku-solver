import math


def check_cross(input_sudoku, row_idx, column_idx):
    print(row_idx, column_idx)
    # TODO: automatically generate this array
    option_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for sub_row in input_sudoku[row_idx - 1]:
        for i in sub_row:
            if i > 0:
                option_list.remove(i)
    sub_row_idx = math.floor((column_idx - 1) / 3) % 3
    col = [row[sub_row_idx][(column_idx - 1) % 3] for row in input_sudoku]
    for j in col:
        if j > 0 and j in option_list:
            option_list.remove(j)
    return option_list


def check_square():
    return 0


def check_items(in_sud, in_opt):
    for row in in_sud:
        for sub_row in row:
            count = 0
            for i in sub_row:
                if i == 0:
                    row_index = in_sud.index(row) + 1
                    column_index = ((row.index(sub_row)) * 3) + 1 + count
                    item_options = check_cross(in_sud, row_index, column_index)
                    print(in_sud.index(row), row.index(sub_row), count, item_options)
                    in_opt[in_sud.index(row)][row.index(sub_row)][count] = item_options
                count += 1
    return 0


if __name__ == '__main__':
    # TODO: read directly from input file
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
    # TODO: create options list of lists automatically
    options = [
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
    ]
    check_items(start, options)
