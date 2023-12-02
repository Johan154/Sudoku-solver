import math
import copy
import sys
import numpy as np

from collections import Counter
from matplotlib import pyplot as plt


def plot_sudoku(sudoku):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))
    ax.grid(which='both')

    # Hide the major and minor ticks
    ax.tick_params(which='both', size=0)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)

    for i in range(1, 9):
        linewidth = 2 if i % 3 == 0 else 0.5
        ax.axhline(i, color='black', linewidth=linewidth)
        ax.axvline(i, color='black', linewidth=linewidth)

    for i in range(9):
        for j in range(9):
            value = sudoku[i][j]
            if value != 0:
                ax.text(j + 0.5, 8.5 - i, str(value),
                        ha='center', va='center', fontsize=12)

    plt.show()


def check_straight(input_list):
    option_list = [i for i in range(1, 10)]
    for j in input_list:
        if j > 0 and j in option_list:
            option_list.remove(j)
    return option_list


def check_square(input_sudoku, row_idx, col_idx):
    option_list = [i for i in range(1, 10)]
    square_row_idx = math.floor(row_idx / 3)
    square_col_idx = math.floor(col_idx / 3)
    for i in range(square_row_idx * 3, (square_row_idx * 3) + 3):
        # print(i, input_sudoku[i][(square_col_idx * 3):(square_col_idx * 3) + 3])
        for j in input_sudoku[i][square_col_idx:square_col_idx + 3]:
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
    row_idx = 0
    for row in input_options:
        col_idx = 0
        for options in row:
            if len(options) == 1:
                input_sudoku[row_idx][col_idx] = options[0]
            col_idx += 1
        row_idx += 1
    return input_sudoku


def check_items(input_sudoku, input_options):
    for row in input_sudoku:
        row_idx = input_sudoku.index(row)
        col_idx = 0
        for item in row:
            if item == 0:
                # Check row, column and square for each 0 value
                row_options = set(check_straight(row))
                col = [line[col_idx] for line in input_sudoku]
                col_options = set(check_straight(col))
                square_options = set(check_square(input_sudoku, row_idx, col_idx))

                # Get the intersection of these 3 lists
                intersection_result = row_options.intersection(col_options, square_options)
                intersection_list = list(intersection_result)

                # Update the options list
                input_options[row_idx][col_idx] = intersection_list

            col_idx += 1
    # for r in input_options:
    #     print(r)
    out_sudoku = check_options(input_sudoku, input_options)
    return out_sudoku, input_options


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

    start_sud = copy.deepcopy(start)
    in_sud = start
    in_opt = options
    out_sud, out_opt = check_items(in_sud, in_opt)
    plot_sudoku(out_sud)

    while out_sud != start_sud:
        start_sud = copy.deepcopy(out_sud)
        out_sud, out_opt = check_items(out_sud, out_opt)
        plot_sudoku(out_sud)

    # for y in out_sud:
    #     print(y)
