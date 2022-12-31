from operator import mul
from functools import reduce
from typing import Any, Set


def iter_low_points(map_lines):
    for y, line in enumerate(map_lines):
        for x, height in enumerate(line):
            if (
                (y == 0 or map_lines[y-1][x] > height) and
                (y == len(map_lines) - 1 or map_lines[y+1][x] > height) and
                (x == 0 or map_lines[y][x-1] > height) and
                (x == len(line) - 1 or map_lines[y][x+1] > height)
            ):
                yield x, y, height

def risk_level(height_levels):
    return sum(level + 1 for level in height_levels)

def parse_height_map(filepath):
    with open(filepath) as input_file:
        lines = input_file.read().splitlines()
    return [list(map(int, line)) for line in lines]


MAX_X = MAX_Y = 99

def find_basin_points(height_map, points_to_check: Set[Any]):
    points_to_check = points_to_check.copy()
    known_points = set()
    
    while len(points_to_check) > 0:
        point = points_to_check.pop()
        x, y = point
        if height_map[y][x] == 9:
            continue
        known_points.add(point)
        if x > 0 and (x - 1, y) not in known_points:
            points_to_check.add((x - 1, y))
        if x < MAX_X and (x + 1, y) not in known_points:
            points_to_check.add((x + 1, y))
        if y > 0 and (x, y - 1) not in known_points:
            points_to_check.add((x, y - 1))
        if y < MAX_Y and (x, y + 1) not in known_points:
            points_to_check.add((x, y + 1))
        
    return known_points




test_lines = [
    [2,1,9,9,9,4,3,2,1,0],
    [3,9,8,7,8,9,4,9,2,1],
    [9,8,5,6,7,8,9,8,9,2],
    [8,7,6,7,8,9,6,7,8,9],
    [9,8,9,9,9,6,5,6,7,8],
]

# print(list(iter_low_points(test_lines)))
# print(risk_level(iter_low_points(test_lines)))

height_map = parse_height_map("day 9.txt")

basins = []
for x, y, height in iter_low_points(height_map):
    basins.append(find_basin_points(height_map, {(x, y)}))

basin_sizes = [len(basin) for basin in basins]
print(sorted(basin_sizes, reverse=True))
print(reduce(mul, sorted(basin_sizes, reverse=True)[:3]))



# print(find_basin_points(height_map, {(0,3)}))
