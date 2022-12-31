import os
import sys
from dataclasses import dataclass

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def load_game(lines):
    monkeys = []
    current = {"inspection-count": 0, "last-i": -1, "items": [None] * 100}
    while (line := next(lines, None)) is not None:
        if line.startswith("Monkey"):
            continue
        if line.startswith("Starting"):
            items_str = line.split(": ")[1]
            for item in [int(item) for item in items_str.split(", ")]:
                current["last-i"] += 1
                current["items"][current["last-i"]] = parse_item(item)
        elif line.startswith("Operation: "):
            operation_str = line.split(" = ")[1]
            current["operation"] = parse_operation(operation_str)
        elif line.startswith("Test"):
            test_str = line.split(": ")[1]
            current["test-divisor"] = parse_test(test_str)
        elif line.startswith("If true"):
            current["if-true"] = int(line.split()[-1])
        elif line.startswith("If false"):
            current["if-false"] = int(line.split()[-1])
        else:
            monkeys.append(current)
            current = {"inspection-count": 0, "last-i": -1, "items": [None] * 100}
    monkeys.append(current)
    return monkeys


def parse_item(worry_level: int):
    DIVISORS = [2, 3, 5, 7, 11, 13, 17, 19]
    return {divisor: worry_level % divisor for divisor in DIVISORS}

def run_round(monkeys, use_limiter=True):
    for monkey in monkeys:
        for i in range(monkey["last-i"]+1):
            item = monkey["items"][i]

            for divisor in item:
                item[divisor] = monkey["operation"](item[divisor]) % divisor
                # if use_limiter:
                #     item[divisor] = ((item[divisor]) // 3) % divisor

            if item[monkey["test-divisor"]] == 0:
                dst = monkeys[monkey["if-true"]]
            else:
                dst = monkeys[monkey["if-false"]]

            dst["last-i"] += 1
            dst["items"][dst["last-i"]] = item
            monkey["inspection-count"] += 1
        monkey["last-i"] = -1

def run_n_rounds(monkeys, n, use_limiter=True):
    for i in range(n):
        run_round(monkeys, use_limiter)
        # if i % 100 == 0:
        #     print(f"Done {i} rounds")


def parse_operation(s):
    if s == "old * old":
        return lambda x: x * x
    if "+" in s:
        args = s.split(" + ")
        b = int(args[1])
        return lambda x: x + b
    if "*" in s:
        args = s.split(" * ")
        b = int(args[1])
        return lambda x: x * b


def parse_test(s):
    return int(s.split(" by ")[1])


def calc_monkey_buisiness(monkeys):
    inspections = [m["inspection-count"] for m in monkeys]
    inspections.sort()
    return inspections[-2] * inspections[-1]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    game = load_game(lines)

    run_n_rounds(game, 20)

    # from pprint import pprint
    # pprint(game)
    print(f"Answer is {calc_monkey_buisiness(game)}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    game = load_game(lines)

    run_n_rounds(game, 10000, False)
    print(f"Answer is {calc_monkey_buisiness(game)}")


part1()
part2()

