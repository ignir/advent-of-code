import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

import re

from common import iter_cleaned_lines


STACKS = [
    'RSLFQ',
    'NZQGPT',
    'SMQB',
    'TGZJHCBQ',
    'PHMBNFS',
    'PCQNSLVG',
    'WCF',
    'QHGZWVPM',
    'GZDLCNR',
]
STACKS = [list(s) for s in STACKS]

MOVE_RE = re.compile(r"move (\d+) from (\d+) to (\d+)")

def move(stacks, count, a, b):
    a = a-1
    b = b-1
    picked_crates = stacks[a][-count:]
    stacks[a] = stacks[a][:-count]
    stacks[b].extend(picked_crates)

def parse_crane_move(s):
    return [int(arg) for arg in MOVE_RE.match(s).groups()]

def print_stacks():
    for stack in STACKS:
        print(stack)
    print()

def part2():
    for line in iter_cleaned_lines(os.path.join(ROOT_DIR, "input_moves.txt")):
        move(STACKS, *parse_crane_move(line))

    print(STACKS)
    print(f"Top crates make: {''.join(s[-1] for s in STACKS)}")

part2()
