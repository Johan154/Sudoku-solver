import math
import copy
import sys
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


def prune_options(ele, prune_row, input_options, sq_idx):
    row_to_prune = input_options[prune_row]
    cell_count = 0
    skip_cells = [0, 1, 2]
    if sq_idx > 0:
        skip_cells = [i + (sq_idx * 3) for i in skip_cells]
    for cell in row_to_prune:
        if ele in cell and cell_count not in skip_cells:
            cell.remove(ele)
        cell_count += 1
    return 0


def check_square_options(input_list, sq_row_idx, sq_col_idx, input_options, sq_idx, input_sudoku):
    opt_per_cell = [cell_opts for row in input_list for cell_opts in row]
    options_list = []
    for subrow in input_list:
        for cell in subrow:
            for option in cell:
                options_list.append(option)
    options_count = Counter(options_list)
    for i in options_count:
        count = options_count[i]
        if count == 1:
            # TODO: use this information to update the current sudoku
            print(f"Element {i} is only possible in {count} cell")
            loc_sq = find_element_index(input_list, i)
            input_sudoku[(sq_idx[0] * 3) + loc_sq[0]][(sq_idx[1] * 3) + loc_sq[1]] = i
            # plot_sudoku(input_sudoku, "target")

        if 2 <= count <= 3:
            row_coords, col_coords = [], []
            for row_index, inner_list in enumerate(opt_per_cell):
                for col_index, element in enumerate(inner_list):
                    if element == i:
                        row_coords.append(row_index % 3)
                        col_coords.append(math.floor(row_index / 3))
            # TODO: use this information to update the current options
            if all(element == row_coords[0] for element in row_coords):
                row_idx = sq_col_idx + row_coords[0]
                transposed_inputs = [[row[i] for row in input_options] for i in range(len(input_options[0]))]
                # print(f"{i} all in the same column ({row_idx})")
                prune_options(i, row_idx, transposed_inputs, sq_idx[0])

                # sys.exit()
            if all(element == col_coords[0] for element in col_coords):
                row_idx = sq_row_idx + col_coords[0]
                # print(f"{i} all in the same row ({row_idx})")
                prune_options(i, row_idx, input_options, sq_idx[1])
    return input_options, input_sudoku


def analyse_square_options(input_options, input_sudoku):
    plot_sudoku(input_sudoku, "start")
    # plot_sudoku_options(input_options, "anaylyse square options")
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            print("\nsquare", round(i/3), round(j/3))
            square = [row[j:j + 3] for row in input_options[i:i + 3]]
            input_options, input_sudoku = check_square_options(square, i, j, input_options, [round(i/3), round(j/3)], input_sudoku)
        # sys.exit()
    plot_sudoku(input_sudoku, "end")
    # plot_sudoku_options(input_options, "end")
    return input_options, input_sudoku


def find_element_index(list_of_lists, target_element):
    for i, sublist in enumerate(list_of_lists):
        for j, cell in enumerate(sublist):
            if target_element in cell:
                print()
                return list_of_lists.index(sublist), j
    return None


def check_options(input_sudoku, input_options):
    print("\nIteration: ", iteration)
    input_options, input_sudoku = analyse_square_options(input_options, input_sudoku)
    transposed_input_options = [list(line) for line in zip(*input_options)]
    row_idx = 0
    for row in input_options:
        analyse_straight_options(row)
        analyse_straight_options(transposed_input_options[row_idx])
        col_idx = 0
        for opt in row:
            if len(opt) == 1:
                input_sudoku[row_idx][col_idx] = opt[0]
            col_idx += 1
        row_idx += 1
    return input_sudoku, input_options


def check_items(input_sudoku, input_options):
    # plot_sudoku(input_sudoku, "check items start")
    # plot_sudoku_options(input_options, "check items start")
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
    out_sudoku, input_options = check_options(input_sudoku, input_options)
    # plot_sudoku(out_sudoku, "check items finish")
    # plot_sudoku_options(out_options, "check items finish")
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

    # Create initial options list
    options = [[[] for j in range(9)] for i in range(9)]
    iteration = 1
    start_sud = copy.deepcopy(start)
    in_sud = start
    in_opt = options
    # plot_sudoku(in_sud)
    out_sud, out_opt = check_items(in_sud, in_opt)
    # out_sud2, out_opt2 = check_items(out_sud, out_opt)

    # while True:
    #     iteration += 1
    #     start_sud = copy.deepcopy(out_sud)
    #     out_sud, out_opt = check_items(out_sud, out_opt)
    #     plot_sudoku_options(out_opt)
