from pprint import pprint

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg


def untangle(combinations):
    combinations = sorted(combinations, key=lambda combination: len(combination))

    one, seven, four = map(frozenset, combinations[:3])
    eight = frozenset(combinations[-1])
    unknown = set(map(frozenset, combinations[3:-1]))
    
    a = seven - one

    for combination in unknown:
        if combination == combination | four:
            nine = combination
            break
    unknown.remove(nine)

    e = eight - nine
    g = nine - four - a

    for combination in unknown:
        if len(combination) == 6 and combination == (combination | one):
            zero = combination
            break
    unknown.remove(zero)

    for combination in unknown:
        if len(combination) == 6 and combination != (combination | one):
            six = combination
            break
    unknown.remove(six)

    d = eight - zero
    b = four - seven - d
    c = one - six
    f = eight - (a | b | c | d | e | g)

    two = eight - b - f
    three = eight - b - e
    five = eight - c - e

    return {
        combination: value 
        for value, combination in 
        enumerate([zero, one, two, three, four, five, six, seven, eight, nine])
    }


def parse_display_value(signal_map, display):
    return int("".join(str(signal_map[frozenset(combination)]) for combination in display))


test = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''

def parse(input_lines):
    result = []
    for line in input_lines:
        signal_str, display_str = line.split(" | ")
        result.append((signal_str.split(), display_str.split()))
    return result


def parse_file(path):
    with open(path) as input_file:
        return parse(input_file.read().splitlines())

def deduce_display_values(data):
    values = []
    for all_signals, display_signals in data:
        signal_map = untangle(all_signals)
        values.append(parse_display_value(signal_map, display_signals))
    return values


print(sum(deduce_display_values(parse_file("day 8.txt"))))

# print(parse_display_value(signal_map, test_value.split()))
