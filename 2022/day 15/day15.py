import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Tuple

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines, Point2d


@dataclass
class Sensor:
    pos: Point2d
    beacon: Point2d

    @property
    def x_coverage(self):
        radius = distance(self.pos, self.beacon)
        return self.pos.x - radius, self.pos.x + radius

    @property
    def y_coverage(self):
        radius = distance(self.pos, self.beacon)
        return self.pos.y - radius, self.pos.y + radius


def parse_sensors(lines: Iterable[str]):
    regexp = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    sensors = []
    for line in lines:
        pos_x, pos_y, beacon_x, beacon_y = map(int, regexp.match(line).groups())
        sensors.append(Sensor(Point2d(pos_x, pos_y), Point2d(beacon_x, beacon_y)))
    return sensors


def distance(p1: Point2d, p2: Point2d) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


def count_known_empty_spots(sensors: List[Sensor], y: int) -> int:
    coverage = list(
        filter(
            None,
            (find_coverage_intersection(sensor, y) for sensor in sensors)
        )
    )
    coverage = union_sections(coverage)
    beacons = (sensor.beacon for sensor in sensors)
    beacons_covered = {beacons for beacon in beacons if beacon.y == y and is_in_sections(y, coverage)}
    return total_length(coverage) - len(beacons_covered)


def count_known_empty_spots_in_range(sensors: List[Sensor], y: int, min_x: int, max_x: int) -> int:
    coverage = []
    for sensor in sensors:
        covered_by_sensor = find_coverage_intersection(sensor, y)
        if not covered_by_sensor:
            continue
        start, end = covered_by_sensor
        coverage.append((max(start, min_x), min(end, max_x)))

    coverage = union_sections(coverage)
    return total_length(coverage)


def find_empty_spots_in_range(sensors: List[Sensor], y: int, min_x: int, max_x: int) -> int:
    coverage = []
    for sensor in sensors:
        covered_by_sensor = find_coverage_intersection(sensor, y)
        if not covered_by_sensor:
            continue
        start, end = covered_by_sensor
        coverage.append((max(start, min_x), min(end, max_x)))

    coverage = union_sections(coverage)
    if len(coverage) > 1:
        return coverage[0][1] + 1, coverage[1][0] - 1

    return None


def union_sections(sections: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if len(sections) <= 1:
        return sections
    sections.sort()
    if sections[1][0] > sections[0][1] + 1:
        return [sections[0]] + union_sections(sections[1:])
    return union_sections([(sections[0][0], max(sections[0][1], sections[1][1]))] + sections[2:])


def total_length(sections: List[Tuple[int, int]]) -> int:
    return sum(b - a + 1 for a, b in sections)


def is_in_sections(x, sections: List[Tuple[int, int]]) -> bool:
    for start, end in sections:
        if start <= x <= end:
            return True
    return False


def clamp(value, low_bound, high_bound):
    if value < low_bound:
        return low_bound
    if value > high_bound:
        return high_bound
    return value


def find_coverage_intersection(sensor: Sensor, y: int):
    min_y, max_y = sensor.y_coverage
    if min_y <= y <= max_y:
        if y == sensor.pos.y:
            return sensor.x_coverage
        if y < sensor.pos.y:
            return min_y - y + sensor.pos.x, y - min_y + sensor.pos.x
        if y > sensor.pos.y:
            return y - max_y + sensor.pos.x, max_y - y + sensor.pos.x
    return None


def test_find_coverage_intersection():
    sensor = Sensor(Point2d(8, 7), Point2d(2, 10))

    assert find_coverage_intersection(sensor, -2) == (8, 8)
    assert find_coverage_intersection(sensor, 0) == (6, 10)
    assert find_coverage_intersection(sensor, 2) == (4, 12)
    assert find_coverage_intersection(sensor, 7) == (-1, 17)
    assert find_coverage_intersection(sensor, 10) == (2, 14)
    assert find_coverage_intersection(sensor, 16) == (8, 8)
    assert find_coverage_intersection(sensor, 20) is None


def test_union_sections():
    assert union_sections([(-5, 5)]) == [(-5, 5)]
    assert union_sections([(5, 10), (0, 1), (-3, 2)]) == [(-3, 2), (5, 10)]
    assert union_sections([(4, 10), (5, 8), (9, 12)]) == [(4, 12)]
    assert union_sections([(4, 10), (0, 1), (5, 5), (5, 8), (9, 12)]) == [(0, 1), (4, 12)]


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    sensors = parse_sensors(lines)

    print(f"Part 1 answer is {count_known_empty_spots(sensors, 2000000)}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    sensors = parse_sensors(lines)
    max_x = 4_000_000
    max_y = 4_000_000

    for y in range(max_y + 1):
        if y % 10000 == 0:
            print(f"Examining {y=}")
        empty_spots = find_empty_spots_in_range(sensors, y, 0, max_x)
        if empty_spots:
            x = empty_spots[0]
            print(f"Beacon is located at {x=}, {y=}")
            break

    print(f"Part 2 answer is {4_000_000 * x + y}")


if __name__ == "__main__":
    part1()
    part2()

