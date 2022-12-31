import os
import sys
from typing import Iterable, List, Tuple, Set

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def to_snafu(value: int) -> str:
    result = ""
    quotient = value
    while True:
        quotient, remainder = divmod(quotient, 5)
        if remainder == 3:
            remainder = "="
            quotient += 1
        elif remainder == 4:
            remainder = "-"
            quotient += 1
        result = str(remainder) + result
        if quotient == 0:
            break
    return result


def to_int(snafu_value: str) -> int:
    result = 0
    for i, digit in enumerate(reversed(snafu_value)):
        if digit == "-":
            digit = -1
        elif digit == "=":
            digit = -2
        else:
            digit = int(digit)
        result += digit * 5 ** i
    return result


def test_to_snafu():
    pairs = '''
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
    '''.strip()

    lines = pairs.split("\n")
    for line in lines:
        decimal, snafu = line.split()
        assert to_snafu(int(decimal)) == snafu


def test_to_int():
    pairs = '''
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37
    '''.strip()

    lines = pairs.split("\n")
    for line in lines:
        snafu, decimal = line.split()
        assert int(decimal) == to_int(snafu)


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))

    total = sum(map(to_int, lines))

    print(f"Part 1 answer is {to_snafu(total)}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    print(f"Part 2 answer is {0}")


if __name__ == "__main__":
    part1()
    part2()

