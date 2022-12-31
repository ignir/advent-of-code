import os
import sys
from dataclasses import dataclass
from enum import Enum, auto

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, Grid


@dataclass
class Point2d:
    x: int
    y: int

from itertools import tee

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def load_obstacles(lines):
    lines = list(lines)
    bounds_min = Point2d(10**10, 10**10)
    bounds_max = Point2d(-10**10, -10**10)

    for line in lines:
        points = line.split(" -> ")
        for point in points:
            x, y = map(int, point.split(","))
            bounds_min.x = min(bounds_min.x, x)
            bounds_min.y = min(bounds_min.y, y)
            bounds_max.x = max(bounds_max.x, x)
            bounds_max.y = max(bounds_max.y, y)

    grid = Grid(bounds_max.x+500, bounds_max.y+6)

    for line in lines:
        points = line.split(" -> ")
        for p0, p1 in pairwise(points):
            x0, y0 = map(int, p0.split(","))
            x1, y1 = map(int, p1.split(","))
            grid.draw_line("#", x0, y0, x1, y1)

    return grid, bounds_min, bounds_max


class SandState(Enum):
    Resting = auto()
    FallenIntoAbyss = auto()


class Simulation:
    def __init__(self, grid: Grid, bounds_max: Point2d):
        self._grid = grid
        self._bounds_max = bounds_max
        self._sand_dropped = 0

    def run_part1(self):
        while True:
            drop_result = self._drop_sand(Point2d(500, 0))
            if drop_result == SandState.FallenIntoAbyss:
                break
            self._sand_dropped += 1
            print(f"{self._sand_dropped} units of sand dropped.")

    def run_part2(self):
        while True:
            self._drop_sand(Point2d(500, 0))
            self._sand_dropped += 1
            print(f"{self._sand_dropped} units of sand dropped.")
            if self._sand_dropped == 100000:
                break
            if self._grid.get(500, 0) == "o":
                break

    def _drop_sand(self, initial: Point2d) -> SandState:
        current_pos = initial
        while True:
            if current_pos.y > self._bounds_max.y:
                return SandState.FallenIntoAbyss
            # Falling down
            if self._grid.get(current_pos.x, current_pos.y + 1) == ".":
                current_pos = Point2d(current_pos.x, current_pos.y + 1)
            # Falling down and left
            elif self._grid.get(current_pos.x - 1, current_pos.y + 1) == ".":
                current_pos = Point2d(current_pos.x - 1, current_pos.y + 1)
            # Falling down and right
            elif self._grid.get(current_pos.x + 1, current_pos.y + 1) == ".":
                current_pos = Point2d(current_pos.x + 1, current_pos.y + 1)
            else:
                self._grid.set(current_pos.x, current_pos.y, "o")
                return SandState.Resting

    @property
    def sand_dropped(self):
        return self._sand_dropped


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    grid, bounds_min, bounds_max = load_obstacles(lines)
    simulation = Simulation(grid, bounds_max)
    simulation.run_part1()

    grid.print(bounds_min.x-5, bounds_max.x+5, bounds_min.y-5, bounds_max.y+5)

    print(f"Part 1 answer is {simulation.sand_dropped}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    grid, bounds_min, bounds_max = load_obstacles(lines)
    grid.add_rows(2)
    grid.draw_line("#", 0, bounds_max.y + 2, grid.max_x, bounds_max.y + 2)
    simulation = Simulation(grid, Point2d(grid.max_x, grid.max_y))
    simulation.run_part2()

    grid.print(bounds_min.x-5, bounds_max.x+5, bounds_min.y-5, bounds_max.y+5)

    print(f"Part 2 answer is {simulation.sand_dropped}")


part1()
part2()

