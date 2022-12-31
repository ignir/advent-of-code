import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def pull_tail(head_pos, tail_pos):
    hx, hy = head_pos
    tx, ty = tail_pos
    if head_pos == tail_pos:
        return tail_pos
    delta = hx-tx, hy-ty
    x_distance, y_distance = abs(delta[0]), abs(delta[1])
    if x_distance <= 1 and y_distance <= 1:
        return tail_pos

    return tx + (delta[0] / x_distance if x_distance > 0 else 0), ty + (delta[1] / y_distance if y_distance > 0 else 0)


def part1():
    moves = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # moves = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    head_pos = tail_pos = (0, 0)
    swept = {(0, 0)}

    for move in moves:
        move_dir, distance = move.split()
        distance = int(distance)
        if move_dir == "L":
            delta = (-1, 0)
        elif move_dir == "R":
            delta = (1, 0)
        elif move_dir == "U":
            delta = (0, 1)
        else:
            delta = (0, -1)
        for step in range(distance):
            head_pos = head_pos[0] + delta[0], head_pos[1] + delta[1]
            tail_pos = pull_tail(head_pos, tail_pos)
            swept.add(tail_pos)
        # print(f"{head_pos=} {tail_pos=}")

    print(f"Positions visited: {len(swept)}")

def part2():
    moves = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    rope = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    swept = {(0, 0)}

    for move in moves:
        move_dir, distance = move.split()
        distance = int(distance)
        if move_dir == "L":
            delta = (-1, 0)
        elif move_dir == "R":
            delta = (1, 0)
        elif move_dir == "U":
            delta = (0, 1)
        else:
            delta = (0, -1)
        for step in range(distance):
            rope[0] = rope[0][0] + delta[0], rope[0][1] + delta[1]
            for i, knot in enumerate(rope[1:], 1):
                rope[i] = pull_tail(rope[i-1], rope[i])
            swept.add(rope[-1])
        # print(f"{head_pos=} {tail_pos=}")

    print(f"Positions visited: {len(swept)}")


part1()
part2()
