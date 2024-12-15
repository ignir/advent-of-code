import os
import sys
from collections import Counter

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))

def sample():
    sample_lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt")))
    listA, listB = parse_lists(sample_lines)
    listA.sort()
    listB.sort()
    return sum(iter_distances(listA, listB))


def part1():
    listA, listB = parse_lists(lines)
    listA.sort()
    listB.sort()
    print(f"Sum of distances is {sum(iter_distances(listA, listB))}")


def part2():
    listA, listB = parse_lists(lines)
    item_counts = Counter(listB)
    similarity_score = 0
    for item in listA:
        similarity_score += item * item_counts[item]
    print(f"Similarity score is {similarity_score}")


def parse_lists(lines):
    listA = []
    listB = []
    for line in lines:
        a, b = line.split()
        listA.append(int(a))
        listB.append(int(b))
    return listA, listB


def iter_distances(listA, listB):
    return (abs(b - a) for a, b in zip(listA, listB))


if __name__ == "__main__":
    sample()
    part1()
    part2()
