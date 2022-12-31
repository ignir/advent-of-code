from collections import defaultdict
import math
import os
from datetime import datetime
import re
import sys
from copy import deepcopy
from typing import Iterable, Optional

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, humanize_timedelta


ROBOT_TYPES = ["ore", "clay", "obsidian", "geode"]


def parse_input(lines):
    blueprints = []
    regexp = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
    for line in lines:
        match = regexp.match(line)
        (
            blueprint_id,
            ore_robot_cost_ore,
            clay_robot_cost_ore,
            obsidian_robot_cost_ore,
            obsidian_robot_cost_clay,
            geode_robot_cost_ore,
            geode_robot_cost_obsidian
        ) = map(int, match.groups())
        blueprints.append({
            "ore": {"ore": ore_robot_cost_ore},
            "clay": {"ore": clay_robot_cost_ore},
            "obsidian": {"ore": obsidian_robot_cost_ore, "clay": obsidian_robot_cost_clay},
            "geode": {"ore": geode_robot_cost_ore, "obsidian": geode_robot_cost_obsidian},
        })
    return blueprints


def sample_blueprints():
    return [
        {
            "ore": {"ore": 4},
            "clay": {"ore": 2},
            "obsidian": {"ore": 3, "clay": 14},
            "geode": {"ore": 2, "obsidian": 7},
        },
        {
            "ore": {"ore": 2},
            "clay": {"ore": 3},
            "obsidian": {"ore": 3, "clay": 8},
            "geode": {"ore": 3, "obsidian": 12},
        },
    ]


class State:
    def __init__(self, blueprint, robots, resources):
        self._blueprint = blueprint
        self._robots = robots
        self._resources = resources

    def build_available_in(self, robot_type) -> Optional[int]:
        for resource in self._blueprint[robot_type]:
            if self._resources[resource] + self._robots[resource] == 0:
                return None
        return max(
            math.ceil((amount - self._resources[res]) / self._robots[res])
            for res, amount in self._blueprint[robot_type].items()
        )

    def can_build(self, robot_type) -> bool:
        for res, amount in self._blueprint[robot_type].items():
            if self._resources[res] < amount:
                return False
        return True

    def build(self, robot_type) -> 'State':
        # Disable check to make runs faster

        # if not self.can_build(robot_type):
        #     raise Exception(f"Not enough resources to construct {robot_type} robot")

        next_state_resources = self._resources.copy()
        next_state_robots = deepcopy(self._robots)
        for resource, amount in self._blueprint[robot_type].items():
            next_state_resources[resource] -= amount
        next_state_robots[robot_type] += 1

        self._add_collected_resources(next_state_resources, self._robots)

        return State(self._blueprint, next_state_robots, next_state_resources)

    def gather_resources(self) -> 'State':
        next_state_resources = self._resources.copy()
        next_state_robots = deepcopy(self._robots)

        self._add_collected_resources(next_state_resources, self._robots)

        return State(self._blueprint, next_state_robots, next_state_resources)

    @staticmethod
    def _add_collected_resources(resources, robots):
        for robot_type, amount in robots.items():
            resources[robot_type] += amount

    def __hash__(self):
        return hash(str(self._robots) + str(self._resources))

    def __eq__(self, other):
        return self._robots == other._robots and self._resources == other._resources


def geode_limit(state: State, minutes_remaining: int) -> int:
    return state._resources["geode"] + state._robots["geode"] * minutes_remaining + sum(range(minutes_remaining))


def dfs(initial: State, steps: int, log=False) -> State:
    start = datetime.now()

    best_state: Optional[State] = None
    known_states = set()
    max_robots = defaultdict(lambda: -1)
    for cost in initial._blueprint.values():
        for resource, amount in cost.items():
            max_robots[resource] = max(max_robots[resource], amount)

    def next_states(state: State) -> Iterable[State]:
        for robot_type in ROBOT_TYPES:
            if state._robots[robot_type] == max_robots[robot_type] or not state.can_build(robot_type):
                continue
            yield state.build(robot_type)
        if not state.can_build("geode"):
            yield state.gather_resources()

    def _dfs(initial: State, steps: int) -> None:
        nonlocal best_state, known_states

        if (steps, initial) in known_states:
            return

        if steps <= 0:
            if best_state is None or best_state._resources["geode"] < initial._resources["geode"]:
                best_state = initial
                if log:
                    print(f"{humanize_timedelta(datetime.now() - start)}: New best state")
                    print(f"  Resources: {best_state._resources}")
                    print(f"  Robots: {best_state._robots}")
                    print()
                return

        following = next_states(initial)
        for state in following:
            if best_state is None or geode_limit(state, steps-1) > best_state._resources["geode"]:
                _dfs(state, steps-1)

        known_states.add((steps, initial))

    _dfs(initial, steps)

    return best_state


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    blueprints = parse_input(lines)
    # blueprints = sample_blueprints()

    total_quality_level = 0
    for id, blueprint in enumerate(blueprints, 1):
        start = datetime.now()
        robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        state = State(blueprint, robots, resources)

        max_geodes = dfs(state, 24)._resources["geode"]
        total_quality_level += max_geodes * id

        print(f"{id}: completed in {humanize_timedelta(datetime.now() - start)}, max geodes: {max_geodes}")

    print(f"Part 1 answer is {total_quality_level}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    blueprints = parse_input(lines)
    # blueprints = sample_blueprints()

    product = 1
    for id, blueprint in enumerate(blueprints[:3], 1):
        start = datetime.now()
        robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        state = State(blueprint, robots, resources)

        max_geodes = dfs(state, 32)._resources["geode"]
        product *= max_geodes

        print(f"{id}: completed in {humanize_timedelta(datetime.now() - start)}, max geodes: {max_geodes}")

    print(f"Part 2 answer is {product}")


if __name__ == "__main__":
    part1()
    part2()
