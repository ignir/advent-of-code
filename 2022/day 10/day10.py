import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def reg_x_value_stream(commands):
    x = 1
    for command in commands:
        if len(command) == 2:
            command, arg = command
            if command == "addx":
                yield x
                yield x
                x += arg
        else:
            yield x

def iter_commands(lines):
    for line in lines:
        if line != "noop":
            command, arg = line.split()
            arg = int(arg)
            # yield "noop"
            # yield "noop"
            yield command, arg
        else:
            yield "noop"


def part1():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample_small.txt"))
    commands = iter_commands(lines)
    strength_sum = 0
    for cycle, signal in enumerate(reg_x_value_stream(commands), 1):
        # 20th, 60th, 100th, 140th, 180th, and 220th cycles
        if cycle in {20, 60, 100, 140, 180, 220}:
            strength_sum += cycle * signal
    print(f"Signal strength sum is {strength_sum}")


def part2():
    lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))
    # lines = iter_cleaned_lines(os.path.join(ROOT_DIR, "sample.txt"))
    sprite_positions = reg_x_value_stream(iter_commands(lines))
    screen = [["."] * 40 for i in range(6)]
    ray_pos = 0
    for cycle, signal in enumerate(sprite_positions, 1):
        ray_x = (cycle - 1) % 40
        ray_y = (cycle - 1) // 40
        if signal - 1 <= ray_x <= signal + 1:
            screen[ray_y][ray_x] = "#"

    for row in screen:
        print("".join(row))



part1()
part2()

