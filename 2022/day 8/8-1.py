import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def load_map(iterable):
    return tuple(tuple(line) for line in iterable)

def is_visible(tree_map, x, y):
    max_x = len(tree_map[0])-1
    max_y = len(tree_map) - 1
    is_visible_from_the_left = all(tree_map[y][left_tree_x] < tree_map[y][x] for left_tree_x in range(0, x))
    is_visible_from_the_right = all(tree_map[y][right_tree_x] < tree_map[y][x] for right_tree_x in range(x+1, max_x+1))
    is_visible_from_the_top = all(tree_map[top_tree_y][x] < tree_map[y][x] for top_tree_y in range(0, y))
    is_visible_from_the_bottom = all(tree_map[bottom_tree_y][x] < tree_map[y][x] for bottom_tree_y in range(y+1, max_y+1))
    return any((is_visible_from_the_left, is_visible_from_the_right, is_visible_from_the_top, is_visible_from_the_bottom))

def count_visible(tree_map):
    count = 0
    for y in range(len(tree_map)):
        for x in range(len(tree_map[y])):
            if is_visible(tree_map, x, y):
                count += 1
    return count

def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    tree_map = load_map(lines)

    print(f"Visible tree total: {count_visible(tree_map)}")

part1()
