import os
import sys
from functools import reduce
from string import ascii_letters

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import chunks, iter_cleaned_lines

PRIORITIES = {letter: priority for letter, priority in zip(ascii_letters, range(1, len(ascii_letters) + 1))}

def find_common_item_type(rucksacks):
    common = reduce(lambda s1, s2: s1 & s2, map(set, rucksacks))
    assert len(common) == 1
    return common.pop()

def part2():
    groups = chunks(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")), 3)
    print(sum(PRIORITIES[find_common_item_type(group)] for group in groups))


part2()
