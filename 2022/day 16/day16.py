import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Tuple

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: List[str]



def build_map(lines) -> dict[str, Valve]:
    valves = {valve.name: valve for valve in map(parse_line, lines)}

    def find_path_length(valve_a, valve_b):
        pass


def solve(network):

    def next_moves(state):
        for valve in state.closed_valves:
            activation_time = route_lengths[state.location][valve]
            if state.time_remaining - activation_time <= 0:
                continue
            yield state.pressure_released + valve.flow_rate * (state.time_remaining - activation_time), valve


def parse_line(line: str) -> Valve:
    regexp = re.compile(r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (((, )?\w{2})+)")
    valve, flow_rate, tunnels = regexp.match(line).groups()[:3]
    flow_rate = int(flow_rate)
    tunnels = tunnels.split(", ")
    return Valve(valve, flow_rate, tunnels)


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    for line in lines:
        print(parse_line(line))

    print(f"Part 1 answer is {0}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    print(f"Part 2 answer is {0}")


if __name__ == "__main__":
    part1()
    part2()

