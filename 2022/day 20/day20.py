import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def parse_input(lines):
    return list(map(int, lines))


def mix(lst: list[int]):
    positions = list(range(len(lst)))
    for i in range(len(lst)):
        move = lst[i]
        cur_position = positions[i]
        dst = (cur_position + move) % (len(lst) - 1)
        if dst > cur_position:
            for j in range(len(lst)):
                if i == j:
                    positions[j] = dst
                elif cur_position <= positions[j] <= dst:
                    positions[j] -= 1
        else:
            for j in range(len(lst)):
                if i == j:
                    positions[j] = dst
                elif dst <= positions[j] <= cur_position:
                    positions[j] += 1

    mixed = [None] * len(lst)
    for i, item in enumerate(lst):
        mixed[positions[i]] = item

    return mixed


def mix2(lst: list[int]):
    positions = list(range(len(lst)))

    for r in range(10):
        for i in range(len(lst)):
            move = (lst[i] * 811589153)
            cur_position = positions[i]
            dst = (cur_position + move) % (len(lst) - 1)
            if dst > cur_position:
                for j in range(len(lst)):
                    if i == j:
                        positions[j] = dst
                    elif cur_position <= positions[j] <= dst:
                        positions[j] -= 1
            else:
                for j in range(len(lst)):
                    if i == j:
                        positions[j] = dst
                    elif dst <= positions[j] <= cur_position:
                        positions[j] += 1
        print(f"{r} round of mixing complete")


    mixed = [None] * len(lst)
    for i, item in enumerate(lst):
        mixed[positions[i]] = item * 811589153

    return mixed



def find_grove_coordinates_sum(mixed: list[int]) -> int:
    zero_index = mixed.index(0)
    return (
        mixed[(1000 + zero_index) % len(mixed)] +
        mixed[(2000 + zero_index) % len(mixed)] +
        mixed[(3000 + zero_index) % len(mixed)]
    )


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    initial = parse_input(lines)

    print(f"Part 1 answer is {find_grove_coordinates_sum(mix(initial))}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    initial = parse_input(lines)
    mixed = mix2(initial)
    # print(mixed)

    print(f"Part 2 answer is {find_grove_coordinates_sum(mixed)}")


if __name__ == "__main__":
    part1()
    part2()

