def iter_cleaned_lines():
    with open("input.txt") as input_data:
        for line in input_data:
            yield line.strip()

def iter_loads():
    load = 0
    for line in iter_cleaned_lines():
        if line:
            load += int(line)
        else:
            yield load
            load = 0


print(sum(sorted(iter_loads())[-3:]))
