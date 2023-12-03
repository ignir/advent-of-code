import os
import string
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def extract_raw_number(line):
    return int(leftmost_digit(line) + rightmost_digit(line))


def extract_number(line):
    return int(leftmost_digit(left_parse_digits(line)) + rightmost_digit(right_parse_digits(line)))


def first_digit(line):
    for c in line:
        if c in string.digits:
            return c


def leftmost_digit(line):
    return first_digit(line)


def rightmost_digit(line):
    return first_digit(reversed(line))


WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
WORDS_TO_DIGITS = {word: str(digit) for digit, word in enumerate(WORDS, 1)}


def left_parse_digits(line):
    if line == "":
        return line
    for word in WORDS:
        if line[:len(word)] == word:
            return WORDS_TO_DIGITS[word] + left_parse_digits(line[len(word):])
    return line[0] + left_parse_digits(line[1:])


def right_parse_digits(line):
    if line == "":
        return line
    for word in WORDS:
        if line[-len(word):] == word:
            return right_parse_digits(line[:-len(word)]) + WORDS_TO_DIGITS[word]
    return right_parse_digits(line[:-1]) + line[-1]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    print(f"Sum of calibration values is {sum(map(extract_raw_number, lines))}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    print(f"Correct sum of calibration values is {sum(map(extract_number, lines))}")


part1()
part2()
