forward = depth = aim = 0

with open("day 2.txt") as input_data:
    for command in input_data:
        direction, change = command.split()
        change = int(change)
        if direction == "forward":
            forward += change
            depth += aim * change
        elif direction == "up":
            aim -= change
        elif direction == "down":
            aim += change
        else:
            raise Exception("WTF?")

print(forward * depth)

