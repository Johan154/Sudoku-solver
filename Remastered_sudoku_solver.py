import itertools
import math
import copy
import sys
import time
import numpy as np

from matplotlib import pyplot as plt
from collections import Counter


def plot_sudoku(sudoku, title):
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
    plt.title(title)
    plt.show()


def plot_sudoku_options(options_grid, title):
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
    plt.title(title)
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


def create_initial_options(input_sudoku):
    # Create empty options list
    options = [[[] for j in range(9)] for i in range(9)]

    # Loop over each cell in the start sudoku
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
                options[row_idx][col_idx] = intersection_list
            col_idx += 1
    return options


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

    input_options = create_initial_options(start)
    plot_sudoku_options(input_options, "Start")
