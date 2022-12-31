import os
import operator
import re
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def parse_input(lines):
    OPERATION_RE = re.compile(r"(\w+) ([+\-*/]) (\w+)")
    OPERATOR_MAP = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    monkeys = {}

    for line in lines:
        name, operation = line.split(": ")
        match = OPERATION_RE.match(operation)
        if match:
            args = match.group(1), match.group(3)
            op = OPERATOR_MAP[match.group(2)]
            monkeys[name] = op, args
        else:
            monkeys[name] = (int(operation), )

    return monkeys


def evaluate(name, pack) -> int:
    monkey = pack[name]
    if callable(monkey[0]):
        return monkey[0](evaluate(monkey[1][0], pack), evaluate(monkey[1][1], pack))
    return monkey[0]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    monkeys = parse_input(lines)

    print(f"Part 1 answer is {evaluate('root', monkeys)}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    monkeys = parse_input(lines)
    monkeys["root"] = operator.sub, monkeys["root"][1]
    # TODO: Переписать на расчёт половинным делением
    monkeys["humn"] = (monkeys["humn"][0] * 837101470 + 3252, )

    print(f"Part 2 evaluation result is {evaluate('root', monkeys)}")
    print(f"Part 2 answer is {monkeys['humn'][0]}")


if __name__ == "__main__":
    part1()
    part2()
