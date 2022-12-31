import os
import sys

from functools import cmp_to_key

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    if isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)):
            if i >= len(right):
                return 1
            if (c := compare(left[i], right[i])) != 0:
                return c
        if len(left) < len(right):
            return -1
        return 0
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])


def get_pairs(lines):
    lines = list(lines)
    return [[eval(p) for p in lines[i:i+2]] for i in range(0, len(lines), 3)]


def get_packets(lines):
    lines = list(lines)
    return [eval(line) for line in lines if line]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))

    index_sum = 0
    for i, pair in enumerate(get_pairs(lines), 1):
        if compare(*pair) == -1:
            index_sum += i

    # pairs = [
    #     ([1,1,3,1,1], [1,1,5,1,1]),
    #     ([[1],[2,3,4]], [[1],4]),
    #     ([], [3]),
    #     ([[[]]], [[]]),
    #     ([9], [[8,7,6]]),
    #     ([[4,4],4,4], [[4,4],4,4,4]),
    #     ([7,7,7,7], [7,7,7]),
    #     ([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]),
    # ]

    # for p in pairs:
    #     print(f"{p=} : {compare(p[0], p[1])}")

    print(f"Part 1 answer is {index_sum}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    packets = get_packets(lines)
    packets.sort(key=cmp_to_key(compare))

    dividers = ([[2]], [[6]])
    cur_divider_index = 0
    decoder_key = 1
    for i, p in enumerate(packets, 1):
        if compare(p, dividers[cur_divider_index]) == 1:
            insertion_index = i + cur_divider_index
            decoder_key *= insertion_index
            cur_divider_index += 1
            if cur_divider_index >= len(dividers):
                break

    print(f"Part 2 answer is {decoder_key}")


part1()
part2()

