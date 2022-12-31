import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from common import iter_cleaned_lines


def find_packet_start_marker(s):
    for i in range(len(s)-4):
        if len(set(s[i:i+4])) == 4:
            return i + 4
    return None

def find_message_start_marker(s):
    for i in range(len(s)-14):
        if len(set(s[i:i+14])) == 14:
            return i + 14
    return None

def part1():
    message = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))[0]
    print(find_packet_start_marker(message))

def part2():
    message = list(iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt")))[0]
    print(find_message_start_marker(message))


part1()
part2()
