from typing import List


test_data = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

class BingoBoard:
    def __init__(self, rows):
        self._board_state = []
        for row in rows:
            board_state_row = [(number, '') for number in row]
            self._board_state.append(board_state_row)
        self._has_won = False
    
    def mark(self, number):
        for row_i, row in enumerate(self._board_state):
            is_number_found = False
            for col_i, (number_in_col, _) in enumerate(row):
                if number_in_col == number:
                    is_number_found = True
                    self._board_state[row_i][col_i] = number, '*'
                    break
            if is_number_found:
                break

    @property
    def has_complete_line(self):
        if self._has_won:
            return True

        for row in self._board_state:
            if all(mark != '' for number, mark in row):
                self._has_won = True
                break

        for col_i in range(len(self._board_state[0])):
            column = (self._board_state[row_i][col_i] for row_i in range(len(self._board_state)))
            if all(mark != '' for number, mark in column):
                self._has_won = True
                break

        return self._has_won

    @property
    def sum_of_unmarked(self):
        return sum(sum(value for value, mark in row if not mark) for row in self._board_state)

    def __str__(self):
        return "\n".join(
            " ".join(f"{mark+str(number):3}" for number, mark in row) 
            for row in self._board_state
        )

def parse(input_lines):
    drawn_numbers = [int(n) for n in input_lines[0].split(",")]
    
    boards = []
    rows = []
    for line in input_lines[2:]:
        if line != '':
            rows.append([int(n) for n in line.split()])
        else:
            boards.append(BingoBoard(rows))
            rows = []
    boards.append(BingoBoard(rows))
    rows = []
    
    return drawn_numbers, boards

def run_game(drawn_numbers, boards: List[BingoBoard]):
    last_board_to_finish = None
    last_board_last_number = None
    for drawn_number in drawn_numbers:
        for board in boards:
            if board.has_complete_line:
                continue
            board.mark(drawn_number)
            if board.has_complete_line:
                last_board_to_finish = board
                last_board_last_number = drawn_number
    return last_board_last_number, last_board_to_finish


def run_on_test_data():
    drawn_numbers, boards = parse(test_data.splitlines())
    return run_game(drawn_numbers, boards)

def run_on_full_data():
    with open("day 4.txt") as input_data:
        input_lines = input_data.read().splitlines()
    drawn_numbers, boards = parse(input_lines)
    return run_game(drawn_numbers, boards)

last_drawn_number, winning_board = run_on_full_data()

print(f"Last drawn: {last_drawn_number}")
print(f"{winning_board}\nHas won: {winning_board.has_complete_line}")
print(f"Score: {winning_board.sum_of_unmarked * last_drawn_number}")


