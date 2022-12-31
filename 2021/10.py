OPENING_BRACKETS = {"[", "(", "{", "<"}
MATCHING_BRACKETS = {"[": "]", "(": ")", "{": "}", "<": ">"}

ILLEGAL_BRACKET_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
COMPLETION_BRACKET_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def find_first_illegal_character(bracket_line):
    bracket_stack = []
    for c in bracket_line:
        if c in OPENING_BRACKETS:
            bracket_stack.append(c)
        else:
            last_opening_bracket = bracket_stack.pop()
            if MATCHING_BRACKETS[last_opening_bracket] != c:
                return c
    return None


def get_completion_string(bracket_line):
    bracket_stack = []
    for c in bracket_line:
        if c in OPENING_BRACKETS:
            bracket_stack.append(c)
        else:
            last_opening_bracket = bracket_stack.pop()
            if MATCHING_BRACKETS[last_opening_bracket] != c:
                raise Exception("Illegal character")
    
    return "".join(MATCHING_BRACKETS[c] for c in reversed(bracket_stack))

def parse(filename):
    with open(filename) as input_file:
        return input_file.read().splitlines()


def calculate_error_score(bracket_lines):
    score = 0
    for line in bracket_lines:
        illegal_character = find_first_illegal_character(line)
        if illegal_character:
            score += ILLEGAL_BRACKET_SCORES[illegal_character]
    return score

def calculate_completion_score(completion_line):
    score = 0

    for c in completion_line:
        score = 5 * score
        score += COMPLETION_BRACKET_SCORES[c]

    return score 


test_input = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''.splitlines()

print(calculate_error_score(test_input))
print(calculate_error_score(parse("day 10.txt")))

completion_scores = []
for line in parse("day 10.txt"):
    if find_first_illegal_character(line):
        continue
    completion_line = get_completion_string(line)
    score = calculate_completion_score(completion_line)
    completion_scores.append(score)
    
completion_scores.sort()
print(completion_scores[len(completion_scores) // 2])