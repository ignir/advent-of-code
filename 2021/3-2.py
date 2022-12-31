readings = []
with open("day 3.txt") as input_data:
    for line in input_data:
        readings.append(line.strip())


def get_most_common_bits(readings):
    bit_counts = [0] * len(readings[0])
    for reading in readings:
        for i, bit in enumerate(reading):
            if bit == "1":
                bit_counts[i] += 1
    return "".join("1" if e >= len(readings) / 2 else "0" for e in bit_counts)

def get_least_common_bits(readings):
    bit_counts = [0] * len(readings[0])
    for reading in readings:
        for i, bit in enumerate(reading):
            if bit == "1":
                bit_counts[i] += 1
    return "".join("0" if e >= len(readings) / 2 else "1" for e in bit_counts)    

def reverse_bits(binary: str) -> str:
    return "".join("0" if bit == "1" else "1" for bit in binary)

def o2_generator_rating(readings, bit_criteria, bit_position=0) -> int:
    filtered = []
    for reading in readings:
        if reading[bit_position] == bit_criteria[bit_position]:
            filtered.append(reading)
    if len(filtered) > 1:
        return o2_generator_rating(filtered, get_most_common_bits(filtered), bit_position+1)
    return int(filtered[0], 2)

def co2_scrubber_rating(readings, bit_criteria, bit_position=0) -> int:
    filtered = []
    for reading in readings:
        if reading[bit_position] == bit_criteria[bit_position]:
            filtered.append(reading)
    if len(filtered) > 1:
        return co2_scrubber_rating(filtered, get_least_common_bits(filtered), bit_position+1)
    return int(filtered[0], 2)    
    
o2_rating = o2_generator_rating(readings, get_most_common_bits(readings))
co2_rating = co2_scrubber_rating(readings, get_least_common_bits(readings))

print(o2_rating)
print(co2_rating)

print(o2_rating * co2_rating)