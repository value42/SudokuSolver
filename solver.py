# -*- coding: utf-8 -*-
from pprint import pprint as pp
import time


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    with open(filename) as f:
        content = f.read()
    digits = [c for c in content if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    """
    lines = len(values) // n
    matrix = [values[i * n: i * n + n] for i in range(lines)]
    return matrix


def get_row(grid, pos):
    return grid[pos[0]]


def get_col(grid, pos):
    return [grid[i][pos[1]] for i in range(9)]


def get_block(grid, pos):
    return [grid[i][j] for i in range(pos[0] // 3 * 3, pos[0] // 3 * 3 + 3) for j in
            range(pos[1] // 3 * 3, pos[1] // 3 * 3 + 3)]


def find_empty_positions(grid):
    """
     Найти первую свободную позицию в пазле
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == ".":
                return i, j
    return 0


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции
    """
    return set('123456789') -\
           set(get_row(grid, pos)) -\
           set(get_col(grid, pos)) -\
           set(get_block(grid, pos))


def solve(grid):
    """ Решение пазла, заданного в grid
    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    position = find_empty_positions(grid)

    if position == 0:
        return grid
    elif find_possible_values(grid, position) == 0:
        return None
    else:
        options = find_possible_values(grid, position)
        for option in options:
            grid[position[0]][position[1]] = option
            if solve(grid):
                return grid
        grid[position[0]][position[1]] = "."


def check_solution(solution: list) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """

    for i in range(9):
        for j in range(9):
            if not (get_row(grid, (i, j)).sort() == get_col(grid, (i, j)).sort() == get_block(grid, (i, j)).sort()):
                return False
    return True


if __name__ == '__main__':
    for fname in ('puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt'):
        grid = read_sudoku(fname)
        start = time.time()
        solve(grid)
        end = time.time()
        print(f'{fname}: {end-start}')
