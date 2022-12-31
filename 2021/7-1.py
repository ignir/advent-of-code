def find_min_fuel(positions):
    positions = sorted(positions)
    median = positions[len(positions) // 2]
    return sum(abs(x - median) for x in positions)

def parse_positions_file(path):
    with open(path) as input_file:
        return [int(x) for x in input_file.read().splitlines()[0].split(",")]


positions = parse_positions_file("day 7.txt")
print(find_min_fuel(positions))