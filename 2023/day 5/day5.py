import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from collections import namedtuple
from typing import Optional

from common import iter_cleaned_lines


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))
# lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt")))


def part1():
    seeds, maps = parse_input(lines)
    lowest_location = min(place_seed(seed, maps) for seed in seeds)
    print(f"Lowest location is {lowest_location}")


def part2():
    seeds, maps = parse_input(lines)
    print(f"")


def parse_input(lines: list[str]):
    seeds: list[int] = list(map(int, lines[0].split(": ")[1].split()))
    maps: list[RangeMap] = []

    cur_map = RangeMap()
    for line in lines[2:]:
        if line.endswith(":"):
            continue
        if line == "":
            maps.append(cur_map)
            cur_map = RangeMap()
        else:
            dst_start, src_start, range_length = (int(number) for number in line.split())
            cur_map.add_range(src_start, dst_start, range_length)
    maps.append(cur_map)

    return seeds, maps


def place_seed(seed, maps):
    dst = seed
    for m in maps:
        dst = m[dst]
    return dst


Range = namedtuple("Range", ["src_start", "src_end", "dst_start", "dst_end"])


class RangeMap:
    def __init__(self):
        self._ranges: list(Range) = []

    def add_range(self, src_start, dst_start, range_len):
        self._ranges.append(Range(src_start, src_start + range_len - 1, dst_start, dst_start + range_len - 1))
        self._ranges.sort()

        src_end = src_start + range_len - 1
        range_len = src_end - src_start + 1

    def __getitem__(self, src_value: int) -> int:
        r = self.find_source_range(src_value)
        if r is None:
            return src_value
        return r.dst_start + src_value - r.src_start

    def find_source_range(self, value: int) -> Optional[Range]:
        for r in self._ranges:
            if r.src_start <= value <= r.src_end:
                return r
        return None

    def squash(self, other: 'RangeMap') -> 'RangeMap':
        result = RangeMap()
        for r in self._ranges:
            other_r = other.find_source_range(r.dst_start)
            result.add_range(r.src_start, other[r.src_start], )



if __name__ == "__main__":
    part1()
    part2()
