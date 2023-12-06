from math import sqrt, ceil, floor, prod
import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))


def part1():
    races = parse_races(lines)
    total = prod(map(count_ways_to_win, races))
    print(f"Number of ways to beat all races is {total}")


def part2():
    races = parse_races(lines)
    time = int("".join(str(r[0]) for r in races))
    record = int("".join(str(r[1]) for r in races))
    total = count_ways_to_win((time, record))
    print(f"Number of ways to beat the races is {total}")


def count_ways_to_win(race):
    time, record = race
    min_hold_time, max_hold_time = find_roots(-1, time, -record)
    if floor(max_hold_time) == max_hold_time:
        max_hold_time = int(max_hold_time - 1)
    else:
        max_hold_time = floor(max_hold_time)
    if ceil(min_hold_time) == min_hold_time:
        min_hold_time = int(min_hold_time + 1)
    else:
        min_hold_time = ceil(min_hold_time)
    return max_hold_time - min_hold_time + 1


def find_roots(a, b, c):
    Dsqrt = sqrt(b*b - 4*a*c)
    return (-b + Dsqrt) / (2*a), (-b - Dsqrt) / (2*a)


def parse_races(lines):
    times = (int(e) for e in lines[0].split(":")[1].split() if e != "")
    records = (int(e) for e in lines[1].split(":")[1].split() if e != "")
    return list(zip(times, records))


part1()
part2()
