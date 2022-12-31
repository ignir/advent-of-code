def iter_cleaned_lines():
    with open("input.txt") as input_data:
        for line in input_data:
            yield line.strip()

HAND_MAP = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}

STRONGER_HANDS = {
    "R": "S",
    "P": "R",
    "S": "P",
}

PLAYER_HAND_VALUES = {"R": 1, "P": 2, "S": 3}

def calculate_player_score(opponent_hand, player_hand):
    opponent_hand = HAND_MAP[opponent_hand]
    player_hand = HAND_MAP[player_hand]
    if opponent_hand == player_hand:
        match_score = 3
    elif STRONGER_HANDS[opponent_hand] == player_hand:
        match_score = 0
    else:
        match_score = 6
    return match_score + PLAYER_HAND_VALUES[player_hand]


def calculate_final_score(matchups):
    return sum(
        calculate_player_score(opponent_hand, player_hand)
        for opponent_hand, player_hand in matchups
    )

print(calculate_final_score(line.split() for line in iter_cleaned_lines()))
