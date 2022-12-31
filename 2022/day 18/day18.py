import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Set

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import Point3d, iter_cleaned_lines


def calculate_surface_area(droplets: Iterable[Point3d]):
    droplets = set(droplets)
    return sum(
        len(get_neighbour_coordinates(droplet) - droplets)
        for droplet in droplets
    )


def find_air_clusters(solids: set[Point3d], start: Point3d, end: Point3d):
    checked_points = solids.copy()

    def _find_whole_air_cluster(point: Point3d) -> set[Point3d]:
        fringe = {point}
        cluster = set()

        while len(fringe) > 0:
            candidate = fringe.pop()
            checked_points.add(candidate)
            if is_in_bounds(candidate, start, end) and candidate not in solids:
                cluster.add(candidate)
                fringe |= get_neighbour_coordinates(candidate) - checked_points

        return cluster

    clusters = []
    for x in range(start.x, end.x + 1):
        for y in range(start.y, end.y + 1):
            for z in range(start.z, end.z + 1):
                point = Point3d(x, y, z)
                if point not in checked_points:
                    clusters.append(_find_whole_air_cluster(point))

    return clusters


def is_inside(cluster_a: set[Point3d], cluster_b: set[Point3d]) -> bool:
    a_min, a_max = find_bounds(cluster_a)
    b_min, b_max = find_bounds(cluster_b)

    return (
        a_min.x > b_min.x and a_min.y > b_min.y and a_min.z > b_min.z and
        a_max.x < b_max.x and a_max.y < b_max.y and a_max.z < b_max.z
    )


def find_bounds(cluster: set[Point3d]) -> Tuple[Point3d, Point3d]:
    start = Point3d(
        min(p.x for p in cluster),
        min(p.y for p in cluster),
        min(p.z for p in cluster),
    )
    end = Point3d(
        max(p.x for p in cluster),
        max(p.y for p in cluster),
        max(p.z for p in cluster),
    )
    return start, end


def is_in_bounds(point: Point3d, low: Point3d, high: Point3d) -> bool:
    return (
        low.x <= point.x <= high.x and
        low.y <= point.y <= high.y and
        low.z <= point.z <= high.z
    )


def get_neighbour_coordinates(point: Point3d) -> set[Point3d]:
    return {
        Point3d(point.x - 1, point.y, point.z),
        Point3d(point.x + 1, point.y, point.z),
        Point3d(point.x, point.y - 1, point.z),
        Point3d(point.x, point.y + 1, point.z),
        Point3d(point.x, point.y, point.z - 1),
        Point3d(point.x, point.y, point.z + 1),
    }


def parse_droplets(lines) -> list[Point3d]:
    droplets = []
    for line in lines:
        droplets.append(Point3d(*map(int, line.split(","))))
    return droplets


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    area = calculate_surface_area(parse_droplets(lines))

    print(f"Part 1 answer is {area}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))

    droplets = set(parse_droplets(lines))
    start, end = find_bounds(droplets)

    clusters = find_air_clusters(droplets, start, end)
    full_area = calculate_surface_area(droplets)
    inner_surface = sum(calculate_surface_area(cluster) for cluster in clusters if is_inside(cluster, droplets))

    print(f"Part 2 answer is {full_area - inner_surface}")


if __name__ == "__main__":
    part1()
    part2()

