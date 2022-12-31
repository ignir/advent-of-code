DOT_MARK = "#"

class Paper:
    def __init__(self, dots):
        self._max_x = max(dot[0] for dot in dots)
        self._max_y = max(dot[1] for dot in dots)

        self._placements = []
        for y in range(self._max_y+1):
            self._placements.append(["."] * (self._max_x + 1))

        for x, y in dots:
            self._placements[y][x] = "#"

    def fold_left(self, fold_along_x):
        for y in range(self._max_y+1):
            for x in range(fold_along_x, self._max_x+1):
                if self._placements[y][x] == "#":
                    self._placements[y][fold_along_x - (x - fold_along_x)] = "#"
                    self._placements[y][x] = "."
        self._max_x = fold_along_x - 1

    def fold_up(self, fold_along_y):
        for y in range(fold_along_y, self._max_y+1):
            for x in range(self._max_x+1):
                if self._placements[y][x] == "#":
                    self._placements[fold_along_y - (y - fold_along_y)][x] = "#"
                    self._placements[y][x] = "."
        self._max_y = fold_along_y - 1

    @property
    def dot_count(self):
        count = 0
        for y in range(self._max_y+1):
            for x in range(self._max_x+1):
                if self._placements[y][x] == "#":
                    count += 1
        return count

    def print(self):
        for y in range(self._max_y+1):
            print("".join(self._placements[y][:self._max_x+1]))


def parse(lines):
    dots = []
    
    for line in lines:
        if line == "":
            break
        x, y = line.split(",")
        dots.append((int(x), int(y)))
    
    return dots

with open("day 13.txt") as input_file:
    dots = parse(input_file.read().splitlines())

paper = Paper(dots)
paper.fold_left(655)
paper.fold_up(447)
paper.fold_left(327)
paper.fold_up(223)
paper.fold_left(163)
paper.fold_up(111)
paper.fold_left(81)
paper.fold_up(55)
paper.fold_left(40)
paper.fold_up(27)
paper.fold_up(13)
paper.fold_up(6)


print(paper.dot_count)
paper.print()