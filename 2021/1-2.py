with open("day 1.txt") as input_data:
    measurements = list(map(int, input_data.read().splitlines()))


sums = []
for start_index in range(len(measurements)):
    window = measurements[start_index:start_index+3]
    if len(window) < 3:
        break
    sums.append(sum(window))

print(sum(int(s2 > s1) for s1, s2 in zip(sums[:-1], sums[1:])))