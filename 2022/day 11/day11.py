import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def load_game(lines):
    monkeys = []
    current = {"inspection-count": 0}
    while (line := next(lines, None)) is not None:
        if line.startswith("Monkey"):
            continue
        if line.startswith("Starting"):
            items_str = line.split(": ")[1]
            current["items"] = [int(item) for item in items_str.split(", ")]
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
            current = {"inspection-count": 0}
    monkeys.append(current)
    return monkeys

def run_round(monkeys):
    for monkey in monkeys:
        for item in monkey["items"]:
            worry_level = monkey["operation"](item)
            worry_level = worry_level // 3
            if worry_level % monkey["test-divisor"] == 0:
                monkeys[monkey["if-true"]]["items"].append(worry_level)
            else:
                monkeys[monkey["if-false"]]["items"].append(worry_level)
            monkey["inspection-count"] += 1
        monkey["items"] = []

def run_n_rounds(monkeys, n):
    for i in range(n):
        run_round(monkeys)


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
    print(f"Answer is {0}")


part1()
part2()

