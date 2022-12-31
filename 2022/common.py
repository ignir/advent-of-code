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


@dataclass
class Point3d:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))


class Grid:
    def __init__(self, width, height, default_char="."):
        self._default_char = "."
        self._max_x = width-1
        self._max_y = height-1
        self._cells = [[default_char] * width for _ in range(height)]

    def print(self, min_x=None, max_x=None, min_y=None, max_y=None):
        min_x = min_x or 0
        max_x = max_x or self._max_x
        for y, row in enumerate(self._cells):
            if min_y and min_y > y:
                continue
            if max_y and max_y < y:
                continue
            print("".join(row[min_x:max_x+1]))

    def set(self, x, y, value):
        self._cells[y][x] = value

    def get(self, x, y) -> Any:
        return self._cells[y][x]

    def draw_line(self, char:str, x0, y0, x1, y1):
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1)+1):
                self.set(x0, y, char)
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1)+1):
                self.set(x, y0, char)
        else:
            raise Exception("Only horizontal and vertical lines are supported.")

    def add_rows(self, rows_to_create: int):
        for _ in range(rows_to_create):
            self._cells.append([self._default_char] * (self._max_x + 1))

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y
