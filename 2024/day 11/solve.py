import os
import sys
from functools import cache

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def part1(input_filename="input.txt"):
    stone_line = list(map(int, list(iter_cleaned_lines(os.path.join(ROOT_DIR, input_filename)))[0].split()))
    stone_line_original = stone_line
    blink_count = 25
    print(f"After {blink_count} blinks line has {final_stone_line_count(stone_line_original, blink_count)} stones")


def part2(input_filename="input.txt"):
    stone_line = list(map(int, list(iter_cleaned_lines(os.path.join(ROOT_DIR, input_filename)))[0].split()))
    stone_line_original = stone_line
    blink_count = 75
    print(f"After {blink_count} blinks line has {final_stone_line_count(stone_line_original, blink_count)} stones")


def blink_line(stone_line: list[int]) -> list[int]:
    new_line = []
    for stone in stone_line:
        if stone == 0:
            new_line.append(1)
        elif is_splittable(stone):
            stone_str = str(stone)
            new_line.append(int(stone_str[:int(len(stone_str) / 2)]))
            new_line.append(int(stone_str[int(len(stone_str) / 2):]))
        else:
            new_line.append(stone * 2024)
    return new_line


def final_stone_line_count(stone_line: list[int], blink_count: int) -> int:
    return sum(final_stone_count(stone, blink_count) for stone in stone_line)


@cache
def final_stone_count(initial_stone: int, blink_count: int):
    if blink_count == 0:
        return 1
    blink_result = blink_stone(initial_stone)
    if len(blink_result) == 1:
        return final_stone_count(blink_result[0], blink_count - 1)
    elif len(blink_result) == 2:
        return final_stone_count(blink_result[0], blink_count - 1) + final_stone_count(blink_result[1], blink_count - 1)
    raise Exception("Хуйня какая-то")
        

def blink_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    if is_splittable(stone):
        stone_str = str(stone)
        return [
            int(stone_str[:int(len(stone_str) / 2)]),
            int(stone_str[int(len(stone_str) / 2):]),
        ]
    return [stone * 2024]


def is_splittable(int) -> bool:
    return len(str(int)) % 2 == 0


if __name__ == "__main__":
    part1("sample.txt")
    part1()
    part2()
    import time
    time.sleep(200)
