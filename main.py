import math
import copy


def check_cross(input_sudoku, row_idx, column_idx):
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


def check_square(input_sudoku, row_idx, column_idx):
    square_row_idx = math.floor(row_idx * 0.33)
    square_col_idx = math.floor((column_idx - 1) / 3)

    option_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(square_row_idx * 3, (square_row_idx * 3) + 3):
        for j in input_sudoku[i][square_col_idx]:
            if j > 0 and j in option_list:
                option_list.remove(j)
    return option_list


def check_options(input_sudoku, input_options):
    for row in input_options:
        for subrow in row:
            for item in subrow:
                if len(item) == 1:
                    row_idx = input_options.index(row)
                    subrow_idx = row.index(subrow)
                    item_idx = subrow.index(item)
                    input_sudoku[row_idx][subrow_idx][item_idx] = item[0]
    return input_sudoku


def check_items(input_sudoku, input_options):
    for row in input_sudoku:
        for sub_row in row:
            count = 0
            for i in sub_row:
                if i == 0:
                    row_index = input_sudoku.index(row) + 1
                    column_index = ((row.index(sub_row)) * 3) + 1 + count
                    item_options_iter1 = check_cross(input_sudoku, row_index, column_index)
                    item_options_iter2 = check_square(input_sudoku, row_index, column_index)
                    input_options[input_sudoku.index(row)][row.index(sub_row)][count] = list(set(item_options_iter1) & set(item_options_iter2))
                count += 1
    out_sudoku = check_options(input_sudoku, input_options)
    return out_sudoku, input_options


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

    options = [[[[] for k in range(3)] for j in range(3)] for i in range(9)]

    start_sud = copy.deepcopy(start)
    in_sud = start
    in_opt = []
    out_sud, out_opt = check_items(in_sud, options)

    while out_sud != start_sud:
        start_sud = copy.deepcopy(out_sud)
        out_sud, out_opt = check_items(out_sud, out_opt)

    for x in out_sud:
        print(x)
