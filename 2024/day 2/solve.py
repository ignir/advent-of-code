import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def part1(input_filename="input.txt"):
    lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, input_filename)))
    level_reports = parse_levels(lines)
    safe_level_count = sum(1 for levels in level_reports if is_safe(levels))
    print(f"{safe_level_count} safe levels")


def part2(input_filename="input.txt"):
    lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, input_filename)))
    level_reports = parse_levels(lines)
    safe_level_count = sum(1 for levels in level_reports if is_safe_with_dampener(levels))
    print(f"{safe_level_count} safe levels if the problem dampener is used")    


def parse_levels(lines):
    return [list(map(int, line.split())) for line in lines]


def is_safe_with_dampener(levels):
    variants = [levels]
    variants.extend(levels[:i] + levels[i + 1:] for i in range(len(levels)))
    return any(map(is_safe, variants))


def is_safe(levels):
    neighbour_pairs = zip(levels[:-1], levels[1:])
    diffs = [b - a for a, b in neighbour_pairs]
    return all(1 <= abs(diff) <= 3 for diff in diffs) and all(d1 * d2 > 0 for d1, d2 in zip(diffs[:-1], diffs[1:]))


if __name__ == "__main__":
    part1("sample.txt")
    part1()
    part2()
