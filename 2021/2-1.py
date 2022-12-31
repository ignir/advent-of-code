
forward = depth = 0

with open("day 2.txt") as input_data:
    for command in input_data:
        direction, change = command.split()
        change = int(change)
        if direction == "forward":
            forward += change
        elif direction == "up":
            depth -= change
        elif direction == "down":
            depth += change
        else:
            raise Exception("WTF?")

print(forward * depth)

