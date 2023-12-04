import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))


def part1():
    cards = map(parse_scratchcard, lines)
    point_total = sum(map(count_points, cards))
    print(f"Point total {point_total}")


def part2():
    cards = list(map(parse_scratchcard, lines))
    card_counts = {index: 1 for index in range(1, len(cards) + 1)}
    for i, card in enumerate(cards, 1):
        for j in range(1, find_winning_number_count(card) + 1):
            card_counts[i + j] += card_counts[i]
    card_total = sum(card_counts.values())
    print(f"You end up with {card_total} scratchcards")


def parse_scratchcard(line):
    index_str, numbers_str = line.split(":")
    winning_numbers_str, card_numbers_str = numbers_str.split("|")
    winning_numbers = {int(number) for number in winning_numbers_str.strip().split() if number != ""}
    card_numbers = {int(number) for number in card_numbers_str.strip().split() if number != ""}
    return winning_numbers, card_numbers


def count_points(card):
    card_winning_numbers_count = find_winning_number_count(card)
    if card_winning_numbers_count == 0:
        return 0
    return 2**(card_winning_numbers_count - 1)


def find_winning_number_count(card):
    winning_numbers, card_numbers = card
    return len(winning_numbers & card_numbers)


part1()
part2()
