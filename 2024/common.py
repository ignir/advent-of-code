from dataclasses import dataclass
from datetime import timedelta
from itertools import tee
from typing import Any


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def iter_cleaned_lines(src="input.txt"):
    with open(src) as input_data:
        for line in input_data:
            yield line.strip()


def chunks(iter, chunk_size):
    chunk = []
    for item in iter:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if len(chunk) != 0:
        yield chunk


def humanize_timedelta(dt: timedelta) -> str:
    return str(dt)


@dataclass
class Point2d:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Point3d:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))


class Grid2023:
    def __init__(self, default_char="."):
        self._default_char = default_char
        self._cells = []
        self._max_x = self._max_y = 0

    @classmethod
    def from_lines(cls, lines, default_char="."):
        grid = Grid2023(default_char=default_char)
        for max_y, line in enumerate(lines):
            grid._max_x = max(grid._max_x, len(line) - 1)
            grid._cells.append(list(line))
        grid._max_y = max_y
        return grid

    def set(self, x, y, value):
        self._cells[y][x] = value

    def get(self, x, y) -> Any:
        return self._cells[y][x]

    def print(self, min_x=None, max_x=None, min_y=None, max_y=None):
        min_x = min_x or 0
        max_x = max_x or self._max_x
        for y, row in enumerate(self._cells):
            if min_y is not None and min_y > y:
                continue
            if max_y is not None and max_y < y:
                continue
            print("".join(row[min_x:max_x+1]))

    def get_neighbour_chars(self, min_x, max_x, min_y, max_y):
        return [self.get(p.x, p.y) for p in self.get_neighbour_positions(min_x, max_x, min_y, max_y)]

    def get_neighbour_positions(self, min_x, max_x, min_y, max_y) -> list[Point2d]:
        candidates: list[Point2d] = []
        for x in range(min_x - 1, max_x + 2):
            candidates.append(Point2d(x, min_y - 1))
            candidates.append(Point2d(x, max_y + 1))
        for y in range(min_y, max_y + 1):
            candidates.append(Point2d(min_x - 1, y))
            candidates.append(Point2d(max_x + 1, y))
        return [c for c in candidates if self._is_on_grid(c.x, c.y)]

    def draw_line(self, char:str, x0, y0, x1, y1):
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1)+1):
                self.set(x0, y, char)
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1)+1):
                self.set(x, y0, char)
        else:
            raise Exception("Only horizontal and vertical lines are supported.")

    def find_all(self, predicate) -> list[Point2d]:
        result = []
        for y in range(self._max_y + 1):
            for x in range(self._max_x + 1):
                if predicate(self.get(x, y)):
                    result.append(Point2d(x, y))
        return result

    def _is_on_grid(self, x, y):
        return 0 <= y <= self._max_y and 0 <= x <= self.max_x

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y
