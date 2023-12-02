import math
import copy
import sys

from collections import Counter


def check_straight(input_list):
    option_list = [i for i in range(1, 10)]
    for j in option_list:
        if j > 0:
            option_list.remove(j)
    return option_list


def check_square(input_sudoku, row_idx, col_idx):
    option_list = [i for i in range(1, 10)]
    square_row_idx = math.floor(row_idx / 3)
    square_col_idx = math.floor(col_idx / 3)
    for i in range(square_row_idx * 3, (square_row_idx * 3) + 3):
        # print(i, input_sudoku[i][(square_col_idx * 3):(square_col_idx * 3) + 3])
        for j in input_sudoku[i][square_row_idx:square_row_idx + 3]:
            if j > 0 and j in option_list:
                option_list.remove(j)
    return option_list


def analyse_row_options(row_opt_list):
    flat_list = [item for sublist in row_opt_list for subsublist in sublist for item in subsublist]
    element_counts = Counter(flat_list)
    element_indices = {element: [] for element in element_counts}
    for i, sublist in enumerate(row_opt_list):
        for j, subsublist in enumerate(sublist):
            for k, item in enumerate(subsublist):
                if item in element_indices:
                    element_indices[item].append((i, j, k))
    unique_element = None
    unique_element_index = None
    for element, indices in element_indices.items():
        if element_counts[element] == 1:
            unique_element = element
            unique_element_index = indices[0]
            break
    if unique_element is not None:
        return [unique_element, unique_element_index]
    else:
        return []


def check_options(input_sudoku, input_options):
    for row in input_options:
        row_idx = input_options.index(row)
        for subrow in row:
            for item in subrow:
                if len(item) == 1:
                    subrow_idx = row.index(subrow)
                    item_idx = subrow.index(item)
                    input_sudoku[row_idx][subrow_idx][item_idx] = item[0]
        sng_occ_row = analyse_row_options(row)
        if sng_occ_row:
            input_sudoku[row_idx][sng_occ_row[1][0]][sng_occ_row[1][1]] = sng_occ_row[0]

    transposed_lists = list(map(list, zip(*input_options)))
    count = 0
    for i, transposed_list in enumerate(transposed_lists):
        count += 1
        transposed_lists = list(map(list, zip(*transposed_list)))
        for i, transposed_list in enumerate(transposed_lists):
            original_list = (transposed_lists[i])
            grouped_list = [original_list[i:i + 3] for i in range(0, len(original_list), 3)]
            sng_occ_col = analyse_row_options(grouped_list)
            if sng_occ_col:
                print(count, sng_occ_col, grouped_list)
                # TODO: count which row should change
                # input_sudoku[row_idx][sng_occ_col[1][0]][sng_occ_col[1][1]] = sng_occ_col[0]
    return input_sudoku


def check_items(input_sudoku, input_options):
    for row in input_sudoku:
        row_idx = input_sudoku.index(row)
        col_idx = 0
        for item in row:
            if item == 0:
                row_options = check_straight(row)
                col = [line[col_idx] for line in input_sudoku]
                col_options = check_straight(col)
                square_options = check_square(input_sudoku, row_idx, col_idx)

                # TODO: get union of the 3 lists
                # sys.exit()
            col_idx += 1

    # out_sudoku = check_options(input_sudoku, input_options)
    # return out_sudoku, input_options


if __name__ == '__main__':
    # TODO: read directly from input file
    # Create initial sudoku
    start = \
        [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    # Create initial options list
    options = [[[] for j in range(9)] for i in range(9)]
    # for row in options:
    #     print(row)

    # start_sud = copy.deepcopy(start)
    # in_sud = start
    # in_opt = []
    # out_sud, out_opt = check_items(in_sud, options)

    check_items(start, options)
    # while out_sud != start_sud:
    #     start_sud = copy.deepcopy(out_sud)
    #     out_sud, out_opt = check_items(out_sud, out_opt)

    # for y in out_opt:
    #     print(y)
