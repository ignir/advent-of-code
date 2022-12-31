def calculate_maneuver_fuel(start_positions, dest):
    return sum(sum(range(abs(dest-x)+1)) for x in start_positions)

def find_min_fuel(positions):
    positions = sorted(positions)
    median = positions[len(positions) // 2]
    return calculate_maneuver_fuel(positions, median)

def parse_positions_file(path):
    with open(path) as input_file:
        return [int(x) for x in input_file.read().splitlines()[0].split(",")]


positions = parse_positions_file("day 7.txt")

destination_candidates = range(min(positions), max(positions) + 1)

print(min(calculate_maneuver_fuel(positions, p) for p in destination_candidates))

# for p in destination_candidates:
#     print(f"Pos {p}. Fuel: {calculate_maneuver_fuel(positions, p)}")

# print(calculate_maneuver_fuel([2], 3))