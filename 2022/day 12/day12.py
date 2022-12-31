import os
import sys

from math import inf

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, Grid


def load_map(lines):
    result = {
        "heights": {},
        "locations": {},
        "max_x": None,
        "max_y": None,
    }
    for y, line in enumerate(lines):
        for x, elevation in enumerate(line):
            if elevation == "S":
                result["locations"]["start"] = x, y
                elevation = "a"
            elif elevation == "E":
                result["locations"]["end"] = x, y
                elevation = "z"
            result["heights"][(x,y)] = ord(elevation)
    result["max_x"] = x
    result["max_y"] = y
    return result


def navigate(height_map, start, end):
    fringe = {start}
    min_steps = {start: 0}
    estimates = {start: rate(start, end)}

    def _get_next():
        min_pos = None
        min_estimate = None
        for pos in fringe:
            if not min_pos or estimates[pos] < min_estimate:
                min_pos = pos
                min_estimate = estimates[pos]
        return min_pos

    while len(fringe) > 0:
        current_pos = _get_next()
        current_steps = min_steps[current_pos]
        if current_pos == end:
            return current_steps
        fringe.remove(current_pos)
        for neighbour in get_moves(height_map, current_pos):
            move_steps = current_steps + 1
            if move_steps < min_steps.get(neighbour, inf):
                min_steps[neighbour] = move_steps
                estimates[neighbour] = move_steps + rate(neighbour, end)
                fringe.add(neighbour)

    return None


def get_moves(height_map, pos):
    x, y = pos
    candidates = []
    current_height = height_map["heights"][pos]
    if x > 0:
        candidates.append((x-1, y))
    if x < height_map["max_x"]:
        candidates.append((x+1, y))
    if y > 0:
        candidates.append((x, y-1))
    if y < height_map["max_y"]:
        candidates.append((x, y+1))
    return [move for move in candidates if height_map["heights"][move] - current_height <= 1]


def rate(pos, dst):
    return abs(dst[0] - pos[0]) + abs(dst[1] - pos[1])


def draw_path(territory, path):
    grid = Grid(territory["max_x"]+1, territory["max_y"]+1)
    for prev, curr in zip(path[:-1], path[1:]):
        if curr[0] > prev[0]:
            c = ">"
        elif curr[0] < prev[0]:
            c = "<"
        elif curr[1] > prev[1]:
            c = "v"
        else:
            c = "^"
        grid.set(prev[0], prev[1], c)
    grid.set(path[-1][0], path[-1][1], "E")
    grid.print()


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    territory = load_map(lines)
    min_steps = navigate(territory, territory["locations"]["start"], territory["locations"]["end"])

    print(f"Answer is {min_steps}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    territory = load_map(lines)
    lowest_points = [pos for pos, height in territory["heights"].items() if height == ord("a")]

    min_steps = min(navigate(territory, p, territory["locations"]["end"]) or inf for p in lowest_points)

    print(f"Answer is {min_steps}")


part1()
part2()

