import os
import sys
from string import ascii_letters

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines

PRIORITIES = {letter: priority for letter, priority in zip(ascii_letters, range(1, len(ascii_letters) + 1))}

def find_packing_error(rucksack):
    half_length = int(len(rucksack) / 2)
    first_compartment, second_compartment = rucksack[:half_length], rucksack[half_length:]
    error = set(first_compartment) & set(second_compartment)
    assert len(error) == 1
    return error.pop()

def calculate_priorities_sum(rucksacks):
    return sum(PRIORITIES[find_packing_error(r)] for r in rucksacks)


print(calculate_priorities_sum(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))))
