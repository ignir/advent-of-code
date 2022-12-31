import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(ROOT_DIR, "..")))

from enum import IntEnum
from itertools import starmap

from common import iter_cleaned_lines


class RPS(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2

    @property
    def beats(self):
        return RPS((self + 2) % 3)

    @property
    def is_beaten_by(self):
        return RPS((self + 1) % 3)


HAND_MAP = {
    "A": RPS.Rock,
    "B": RPS.Paper,
    "C": RPS.Scissors,
}


def calculate_match_score(opponent_hand, match_result):
    opponent_hand = HAND_MAP[opponent_hand]
    if match_result == "X":
        player_hand = opponent_hand.beats
        match_score = 0
    elif match_result == "Y":
        player_hand = opponent_hand
        match_score = 3
    else:
        player_hand = opponent_hand.is_beaten_by
        match_score = 6
    return match_score + (player_hand + 1)


def calculate_final_score(matchups):
    return sum(starmap(calculate_match_score, matchups))


print(calculate_final_score(line.split() for line in iter_cleaned_lines(os.path.join(ROOT_DIR, "input.txt"))))
