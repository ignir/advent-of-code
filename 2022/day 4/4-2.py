import os
import sys

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

def has_overlap(span_a, span_b):
    return span_a[0] <= span_b[1] and span_a[1] >= span_b[0]


def part2():
    counter = 0
    for sections_a, sections_b in get_section_span_pairs(os.path.join(ROOT_DIR, "input.txt")):
        if has_overlap(sections_a, sections_b):
            counter += 1
    print(counter)


part2()
