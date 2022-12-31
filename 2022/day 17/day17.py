import os
import sys
from typing import Iterable, List, Tuple, Set

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))

    print(f"Part 1 answer is {0}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    print(f"Part 2 answer is {0}")


if __name__ == "__main__":
    part1()
    part2()

