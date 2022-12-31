def simulate(lanternfish, days_to_run):
    for day in range(1, days_to_run+1):
        new_spawn_count = 0
        for i, timer in enumerate(lanternfish):
            if timer == 0:
                new_spawn_count += 1
                lanternfish[i] = 6
            else:
                lanternfish[i] = timer - 1
        lanternfish.extend([8] * new_spawn_count)
        print(f"After day {day}")
        # print(lanternfish)
    print(f"Lanternfish total: {len(lanternfish)}")

def simulate2(lanternfish, days_to_run):
    fish_counts = [0] * 9
    for fish in lanternfish:
        fish_counts[fish] += 1
    for day in range(1, days_to_run+1):
        ready_to_spawn_count = fish_counts[0]        
        for timer_value in range(0, 8):
            fish_counts[timer_value] = fish_counts[timer_value+1]
        fish_counts[6] += ready_to_spawn_count
        fish_counts[8] = ready_to_spawn_count
        print(f"After day {day}")
    print(f"Lanternfish total: {sum(fish_counts)}")

def parse_file(filename):
    with open(filename) as input_data:
        lanternfish = [int(f) for f in input_data.read()[:-1].split(",")]
    return lanternfish

# simulate2([3,4,3,1,2], 80)

# print(parse_file("day 6.txt"))
simulate2(parse_file("day 6.txt"), 256)