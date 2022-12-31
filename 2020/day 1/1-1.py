numbers = []
with open('input.txt') as input_file:
    for line in input_file:
        numbers.append(int(line))

for i in range(len(numbers)):
    a = numbers[i]
    for b in numbers[i+1:]:
        if a + b == 2020:
            print(f"{a} + {b} = 2020. a * b = {a * b}")
