with open("day 1.txt") as input_data:
    measurements = list(map(int, input_data.read().splitlines()))

pairs = zip(measurements[:-1], measurements[1:])

print(sum(int(m2 > m1) for m1, m2 in pairs))
