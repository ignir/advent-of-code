bit_counts = [0] * 12

with open("day 3.txt") as input_data:
    for line in input_data:
        for i, bit in enumerate(line):
            if bit == "1":
                bit_counts[i] += 1

print(bit_counts)

gamma_rate = int("".join("1" if e > 500 else "0" for e in bit_counts), 2)
epsilon_rate = int("".join("0" if e > 500 else "1" for e in bit_counts), 2)

print(gamma_rate * epsilon_rate)

def o2_generator_rating(bit_counts):
    