import os
import re
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, pairwise


def parse_input(lines):
    lines = list(lines)
    template = lines[0]
    rules = {}
    regex = re.compile(r"(\w{2}) -> (\w)")
    for rule_line in lines[2:]:
        left, right = regex.match(rule_line).groups()
        rules[left] = right
    return template, rules


def polymerize(polymer, rules):
    insertions = []
    for a, b in pairwise(polymer):
        combo = a + b
        insertions.append(rules.get(combo, ''))
    result = polymer[0]
    for new, original in zip(insertions, polymer[1:]):
        result += new + original
    return result


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    polymer, rules = parse_input(lines)

    for step in range(10):
        polymer = polymerize(polymer, rules)
        print(polymer)


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    print(f"Part 2 answer is {0}")


if __name__ == "__main__":
    part1()
    part2()
