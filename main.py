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


def prune_options_same_dir(ele, prune_row, input_options, sq_idx):
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
            loc_sq = find_element_index(input_list, i)
            row_id = (sq_idx[0] * 3) + loc_sq[0]
            col_id = (sq_idx[1] * 3) + loc_sq[1]
            print(f"Element {i} is only possible in {count} cell in row {row_id} and column {col_id}")
            input_sudoku[row_id][col_id] = i
            input_options[row_id][col_id] = []
            prune_options_ele_added(input_options, row_id, col_id, i)
            transposed_inputs = [[line[j] for line in input_options] for j in range(len(input_options[0]))]
            prune_options_ele_added(transposed_inputs, col_id, row_id, i)
        if 2 <= count <= 3:
            row_coords, col_coords = [], []
            for row_index, inner_list in enumerate(opt_per_cell):
                for col_index, element in enumerate(inner_list):
                    if element == i:
                        row_coords.append(row_index % 3)
                        col_coords.append(math.floor(row_index / 3))
            if all(element == row_coords[0] for element in row_coords):
                row_idx = sq_col_idx + row_coords[0]
                transposed_inputs = [[row[i] for row in input_options] for i in range(len(input_options[0]))]
                # print(f"{i} all in the same column ({row_idx})")
                prune_options_same_dir(i, row_idx, transposed_inputs, sq_idx[0])
            if all(element == col_coords[0] for element in col_coords):
                row_idx = sq_row_idx + col_coords[0]
                # print(f"{i} all in the same row ({row_idx})")
                prune_options_same_dir(i, row_idx, input_options, sq_idx[1])
    return input_options, input_sudoku


def check_square_equals(input_list, sq_row_idx, sq_col_idx, input_options, sq_idx):
    # TODO: make this working for all lengths
    # TODO: check if they are on the same row or column
    cell_list = [element for innerList in input_list for element in innerList]
    for a, b in itertools.combinations(cell_list, 2):
        if a == b and a and b:
            if len(a) == 2:
                indices = [i for i, x in enumerate(cell_list) if x == a]
                print(f"Matching inputs found {a} with indices {indices}")
                for j in range(len(cell_list)):
                    if cell_list[j] and j not in indices:
                        cell_list[j] = list(set(cell_list[j]).difference(a))
                row_coords, col_coords = [], []
                for row_index, inner_list in enumerate(cell_list):
                    for col_index, element in enumerate(inner_list):
                        if element in a:
                            row_coords.append(row_index % 3)
                            col_coords.append(math.floor(row_index / 3))
                if all(element == row_coords[0] for element in row_coords):
                    for i in a:
                        row_idx = sq_col_idx + row_coords[0]
                        transposed_inputs = [[row[p] for row in input_options] for p in range(len(input_options[0]))]
                        # print(f"{i} all in the same column ({row_idx})")
                        prune_options_same_dir(i, row_idx, transposed_inputs, sq_idx[0])
                if all(element == col_coords[0] for element in col_coords):
                    for i in a:
                        row_idx = sq_row_idx + col_coords[0]
                        # print(f"{i} all in the same row ({row_idx})")
                        prune_options_same_dir(i, row_idx, input_options, sq_idx[1])
    input_list = [cell_list[i:i+3] for i in range(0, len(cell_list), 3)]
    return input_list


def analyse_square_options(input_options, input_sudoku):
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            print("\nsquare", round(i/3), round(j/3))
            square = [row[j:j + 3] for row in input_options[i:i + 3]]
            input_options, input_sudoku = check_square_options(square, i, j, input_options, [round(i/3), round(j/3)], input_sudoku)
            new_square = check_square_equals(square, i, j, input_options, [round(i/3), round(j/3)])
            if square != new_square:
                start_row, start_col = i, j
                for y in range(3):
                    for z in range(3):
                        input_options[start_row + y][start_col + z] = new_square[y][z]
    return input_options, input_sudoku


def find_element_index(list_of_lists, target_element):
    for i, sublist in enumerate(list_of_lists):
        for j, cell in enumerate(sublist):
            if target_element in cell:
                return list_of_lists.index(sublist), j
    return None


def prune_options_ele_added(input_options, row_idx, col_idx, ele):
    for cell in input_options[row_idx]:
        if cell and ele in cell:
            cell.remove(ele)
    i = math.floor(row_idx / 3) * 3
    j = math.floor(col_idx / 3) * 3
    square = [row[j:j + 3] for row in input_options[i:i + 3]]
    for subrow in square:
        for cell in subrow:
            if cell and ele in cell:
                cell.remove(ele)


def check_options(input_sudoku, input_options):
    print("\nIteration: ", iteration)
    input_options, input_sudoku = analyse_square_options(input_options, input_sudoku)
    row_idx = 0
    for row in input_options:
        col_idx = 0
        for opt in row:
            if len(opt) == 1:
                input_sudoku[row_idx][col_idx] = opt[0]
                input_options[row_idx][col_idx] = []
                # plot_sudoku(input_sudoku, f"inbetween version {iteration}")
                print(f"Updated sudoku with element {opt[0]} in row {row_idx} and column {col_idx}")
                prune_options_ele_added(input_options, row_idx, col_idx, opt[0])
                # plot_sudoku_options(input_options, f"inbetween version {iteration}")
                transposed_inputs = [[line[i] for line in input_options] for i in range(len(input_options[0]))]
                # plot_sudoku_options(transposed_inputs, f"inbetween version {iteration}")
                prune_options_ele_added(transposed_inputs, col_idx, row_idx, opt[0])
            col_idx += 1
        row_idx += 1
    return input_sudoku, input_options


def check_items(input_sudoku, input_options):
    if iteration == 1:
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
    out_sud, out_opt = check_items(in_sud, in_opt)
    # plot_sudoku(out_sud, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 2
    out_sud2, out_opt2 = check_items(out_sud, out_opt)
    # plot_sudoku(out_sud2, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt2, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 3
    out_sud3, out_opt3 = check_items(out_sud2, out_opt2)
    # plot_sudoku(out_sud3, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt3, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 4
    out_sud4, out_opt4 = check_items(out_sud3, out_opt3)
    # plot_sudoku(out_sud4, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt4, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 5
    out_sud5, out_opt5 = check_items(out_sud4, out_opt4)
    # plot_sudoku(out_sud5, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt5, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 6
    out_sud6, out_opt6 = check_items(out_sud5, out_opt5)
    # plot_sudoku(out_sud6, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt6, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 7
    out_sud7, out_opt7 = check_items(out_sud6, out_opt6)
    # plot_sudoku(out_sud7, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt7, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 8
    out_sud8, out_opt8 = check_items(out_sud7, out_opt7)
    # plot_sudoku(out_sud8, f"out_sud {iteration}")
    # plot_sudoku_options(out_opt8, f"out opt {iteration}")

    time.sleep(0.3)
    iteration = 9
    out_sud9, out_opt9 = check_items(out_sud8, out_opt8)
    plot_sudoku(out_sud9, f"out_sud {iteration}")
    plot_sudoku_options(out_opt9, f"out opt {iteration}")
