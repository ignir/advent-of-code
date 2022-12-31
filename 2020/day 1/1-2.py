numbers = []
with open('input.txt') as input_file:
    for line in input_file:
        numbers.append(int(line))

for i in range(len(numbers)):
    a = numbers[i]
    for b in numbers[i+1:]:
        for c in numbers[i+2:]:
            if a + b + c == 2020:
                print(f"{a} + {b} + {c} = 2020. a * b * c = {a * b * c}")
