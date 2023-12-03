import os
import string
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, Grid2023, Point2d


lines = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))
schematic = Grid2023.from_lines(lines)
NON_SYMBOL_CHARS = set(string.digits + schematic._default_char)


def part1():
    symbols = schematic.find_all(lambda c: c not in NON_SYMBOL_CHARS)
    part_numbers_sum = sum(sum(get_neighbour_numbers(schematic, symbol)) for symbol in symbols)
    print(f"Part numbers sum is {part_numbers_sum}")


def part2():
    asterisks: list[Point2d] = schematic.find_all(lambda c: c == "*")
    gear_ratio_sum = 0
    for gear_candidate in asterisks:
        neighbour_parts = get_neighbour_numbers(schematic, gear_candidate)
        if len(neighbour_parts) == 2:
            gear_ratio_sum += neighbour_parts[0] * neighbour_parts[1]
    print(f"Gear ratio sum is {gear_ratio_sum}")


def get_neighbour_numbers(schematic: Grid2023, pos: Point2d) -> list[int]:
    numbers = []
    unchecked_positions = set(schematic.get_neighbour_positions(pos.x, pos.x, pos.y, pos.y))
    while len(unchecked_positions) > 0:
        current_pos = unchecked_positions.pop()
        number_span = find_number_span(schematic, current_pos)
        if number_span is None:
            continue
        start, end = number_span
        unchecked_positions -= {Point2d(x, start.y) for x in range(start.x, end.x + 1)}
        numbers.append(int("".join(schematic._cells[current_pos.y][start.x : end.x + 1])))
    return numbers


def find_number_span(schematic: Grid2023, pos: Point2d):
    if schematic.get(pos.x, pos.y) not in string.digits:
        return None
    start = end = pos.x
    for x in range(pos.x - 1, -1, -1):
        if schematic.get(x, pos.y) not in string.digits:
            break
        start = x
    for x in range(pos.x + 1, schematic.max_x + 1):
        if schematic.get(x, pos.y) not in string.digits:
            break
        end = x
    return Point2d(start, pos.y), Point2d(end, pos.y)


part1()
part2()
