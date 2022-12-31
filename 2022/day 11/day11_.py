import os
import sys

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
                current["items"][current["last-i"]] = item
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

def run_round(monkeys):
    for monkey in monkeys:
        for i in range(monkey["last-i"]+1):
            item = monkey["items"][i]
            worry_level = monkey["operation"](item)
            # worry_level = worry_level // 3
            if monkey["test-divisor"](worry_level):
                dst = monkeys[monkey["if-true"]]
            else:
                dst = monkeys[monkey["if-false"]]
            dst["last-i"] += 1
            dst["items"][dst["last-i"]] = worry_level
            monkey["inspection-count"] += 1
        monkey["last-i"] = -1

def run_n_rounds(monkeys, n):
    for i in range(n):
        run_round(monkeys)
        if i % 100 == 0:
            print(f"Done {i} rounds")


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

# Test: divisible by 2
# Test: divisible by 3
# Test: divisible by 5
# Test: divisible by 7

def is_divisible_by_2(value):
    return int(str(value)[-1]) % 2 == 0
    return (value % 10) % 2 == 0

def is_divisible_by_3(value):
    return sum(int(d) for d in str(value)) % 3 == 0

def is_divisible_by_5(value):
    # last_digit = value % 10
    last_digit = int(str(value)[-1])
    return last_digit == 0 or last_digit == 5

def is_divisible_by_7(value):
    digits = str(value)
    digits = "0"*(3 - len(digits) % 3) + digits
    result = 0
    positive = True
    for i in range(0, len(digits), 3):
        triplet = int(digits[i:i+3])
        if positive:
            result += triplet
        else:
            result -= triplet
        positive = not positive
    return result % 7 == 0

# Test: divisible by 11
def is_divisible_by_11(value):
    digits = str(value)
    digits = "0"*(3 - len(digits) % 3) + digits
    result = 0
    positive = True
    for i in range(0, len(digits), 3):
        triplet = int(digits[i:i+3])
        if positive:
            result += triplet
        else:
            result -= triplet
        positive = not positive
    return result % 11 == 0

# Test: divisible by 13
def is_divisible_by_13(value):
    digits = str(value)
    digits = "0"*(3 - len(digits) % 3) + digits
    result = 0
    positive = True
    for i in range(0, len(digits), 3):
        triplet = int(digits[i:i+3])
        if positive:
            result += triplet
        else:
            result -= triplet
        positive = not positive
    return result % 13 == 0

# Test: divisible by 17
def is_divisible_by_17(value):
    digits = str(value)
    return (int(digits[:-1]) - 5*int(digits[-1])) % 17 == 0

# Test: divisible by 19
def is_divisible_by_19(value):
    digits = str(value)
    return (int(digits[:-1]) + 2*int(digits[-1])) % 19 == 0


TEST_MAP = {
    2: is_divisible_by_2,
    3: is_divisible_by_3,
    5: is_divisible_by_5,
    7: is_divisible_by_7,
    11: is_divisible_by_11,
    13: is_divisible_by_13,
    17: is_divisible_by_17,
    19: is_divisible_by_19
}



def parse_test(s):
    return TEST_MAP[int(s.split(" by ")[1])]

def calc_monkey_buisiness(monkeys):
    inspections = [m["inspection-count"] for m in monkeys]
    inspections.sort()
    return inspections[-2] * inspections[-1]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    game = load_game(lines)

    run_n_rounds(game, 10000)

    # from pprint import pprint
    # pprint(game)
    print(f"Answer is {calc_monkey_buisiness(game)}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))

    # run_n_rounds(game, 10000)
    print(f"Answer is {0}")


part1()
part2()

