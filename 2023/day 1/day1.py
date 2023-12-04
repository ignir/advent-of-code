import os
import string
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))


def part1():
    def extract_raw_number(line):
        return int(first_digit(line) + first_digit(reversed(line)))

    calibration_values_sum = sum(map(extract_raw_number, lines))
    print(f"Sum of calibration values is {calibration_values_sum}")
    return calibration_values_sum


def part2():
    WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    WORDS_TO_DIGITS = {word: str(digit) for digit, word in enumerate(WORDS, 1)}
    REVERSED_WORDS_TO_DIGITS = {word[::-1]: str(digit) for digit, word in enumerate(WORDS, 1)}

    def extract_number(line):
        return int(first_digit(parse_digits(line, WORDS_TO_DIGITS)) + first_digit(parse_digits(line[::-1], REVERSED_WORDS_TO_DIGITS)))

    calibration_values_sum = sum(map(extract_number, lines))
    print(f"Correct sum of calibration values is {calibration_values_sum}")
    return calibration_values_sum


def first_digit(line):
    for c in line:
        if c in string.digits:
            return c


def parse_digits(line, words_to_digits):
    if line == "":
        return line
    for word, digit in words_to_digits.items():
        if line[:len(word)] == word:
            return digit + parse_digits(line[len(word):], words_to_digits)
    return line[0] + parse_digits(line[1:], words_to_digits)


if __name__ == "__main__":
    part1()
    part2()
