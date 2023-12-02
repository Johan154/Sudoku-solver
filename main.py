import math
import copy
import numpy as np

from matplotlib import pyplot as plt
from collections import Counter


def plot_sudoku(sudoku):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))
    ax.grid(which='both')
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


def plot_sudoku_options(options_grid):
    rows = len(options_grid)
    cols = len(options_grid[0])
    options_matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            opts = options_grid[i][j]
            opts.sort()
            options_matrix[i, j] = len(opts)
    plt.imshow(options_matrix, cmap='viridis', interpolation='nearest')
    for i in range(rows):
        for j in range(cols):
            opts = options_grid[i][j]
            if opts:
                plt.text(j, i, ' '.join(map(str, opts)), color='white', ha='center', va='center', fontsize=7)
    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.title('Sudoku Options')
    plt.colorbar(label='Number of Options')
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
        for j in input_sudoku[i][(square_col_idx * 3):(square_col_idx * 3) + 3]:
            if j > 0 and j in option_list:
                option_list.remove(j)
    return option_list


def analyse_straight_options(input_list):
    sng_options = []
    all_options = [item for sublist in input_list for item in sublist]
    for item_opt in input_list:
        for opt in item_opt:
            all_options.append(opt)
    count_all_options = Counter(all_options)
    for i in count_all_options:
        count = count_all_options[i]
        if count == 1:
            # TODO: use this information to update the current sudoku
            print(iteration, find_element_index(input_list, i))
            sng_options.append(i)
        # print(i, count_all_options[i])
    # print("\n")


def analyse_square_options(input_options):
    # TODO:
    # loop over squares
    # check for each squares how many times an element can be used
    # check for elements that are only possible 2 or 3 times if the are on the same row or column
    return 0


def find_element_index(list_of_lists, target_element):
    for i, sublist in enumerate(list_of_lists):
        if target_element in sublist:
            return i, sublist.index(target_element)
    return None


def check_options(input_sudoku, input_options):
    print("\nIteration: ", iteration)
    # TODO: make function that checks if one number can only be used in one cell within a square
    # TODO: loop over squares for options list

    transposed_input_options = [list(line) for line in zip(*input_options)]
    row_idx = 0
    for row in input_options:
        analyse_straight_options(row)
        analyse_straight_options(transposed_input_options[row_idx])
        # TODO: make function that checks if one number is only possible in one direction, e.g. 6 only possible in col 8
        col_idx = 0
        for opt in row:
            if len(opt) == 1:
                input_sudoku[row_idx][col_idx] = opt[0]
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
    out_sudoku = check_options(input_sudoku, input_options)
    return out_sudoku, input_options




if __name__ == '__main__':
    # TODO: read directly from input file
    # Create initial sudoku
    start = \
        [[0, 6, 0, 0, 0, 0, 0, 9, 1],
         [0, 2, 8, 7, 0, 0, 0, 0, 3],
         [1, 0, 0, 4, 0, 0, 8, 0, 0],
         [0, 0, 0, 5, 0, 0, 0, 0, 2],
         [5, 0, 0, 2, 0, 0, 0, 0, 4],
         [0, 3, 0, 0, 0, 6, 0, 0, 7],
         [0, 7, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 8, 0, 6, 0, 0],
         [3, 0, 4, 0, 2, 0, 0, 0, 0]]

    # plot_sudoku(start)
    # Create initial options list
    options = [[[] for j in range(9)] for i in range(9)]
    iteration = 1
    start_sud = copy.deepcopy(start)
    in_sud = start
    in_opt = options
    out_sud, out_opt = check_items(in_sud, in_opt)

    plot_sudoku_options(out_opt)
    while out_sud != start_sud:
        iteration += 1
        start_sud = copy.deepcopy(out_sud)
        out_sud, out_opt = check_items(out_sud, out_opt)
    # plot_sudoku(out_sud)
