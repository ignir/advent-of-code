import os
import sys
from functools import reduce
from string import ascii_letters

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def get_section_span_pairs(src):
    for line in iter_cleaned_lines(src):
        sections_a, sections_b = line.split(",")
        yield _parse_sections(sections_a), _parse_sections(sections_b)

def _parse_sections(sections: str):
    start, end = sections.split("-")
    return int(start), int(end)

def fully_contains(outer_span, inner_span):
    return outer_span[0] <= inner_span[0] and outer_span[1] >= inner_span[1]

def part1():
    counter = 0
    for span_a, span_b in get_section_span_pairs(os.path.join(ROOT_DIR, "input.txt")):
        if fully_contains(span_a, span_b) or fully_contains(span_b, span_a):
            counter += 1
    print(counter)


part1()
