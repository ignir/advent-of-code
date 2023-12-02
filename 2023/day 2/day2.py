import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def parse_game(line):
    game_id_str, pulls_str = line.split(": ")
    subsets = pulls_str.split("; ")
    return {
        "id": int(game_id_str.split()[-1]),
        "subsets": list(map(parse_subset, subsets))
    }

def parse_subset(s):
    result = {}
    for group in s.split(", "):
        count, color = group.split(" ")
        result[color] = int(count)
    return result

def is_possible(game):
    return all(
        subset.get("red", 0) <= 12 and subset.get("green", 0) <= 13 and subset.get("blue", 0) <= 14
        for subset in game["subsets"]
    )

def calculate_power(game):
    return (
        max(subset.get("red", 0) for subset in game["subsets"]) *
        max(subset.get("green", 0) for subset in game["subsets"]) *
        max(subset.get("blue", 0) for subset in game["subsets"])
    )

def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    id_sum = sum(game["id"] for game in map(parse_game, lines) if is_possible(game))
    print(f"Sum of ids is {id_sum}")

def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    power_sum = sum(calculate_power(game) for game in map(parse_game, lines))
    print(f"Power sum is {power_sum}")


part1()
part2()
