pairs = []
with open("08/input.txt") as f:
    patterns_and_digits = f.read().strip().splitlines()
    for pd in patterns_and_digits:
        patterns, digits = pd.split(' | ')
        pair = {
            'patterns': patterns.split(),
            'digits': digits.split()
        }
        pairs.append(pair)


def get_diff(a, b):
    diff = set(list(a)) - set(list(b))
    return ''.join(diff)


def solve_known_digits(patterns, solved):
    remaining_patterns = []
    for p in patterns:
        l = len(p)
        if l == 2:
            solved[1] = p
        elif l == 3:
            solved[7] = p
        elif l == 4:
            solved[4] = p
        elif l == 7:
            solved[8] = p
        else:
            remaining_patterns.append(p)

    return (remaining_patterns, solved)


def solve_six(patterns, solved):
    remaining_patterns = []
    one = solved[1]
    for i, p in enumerate(patterns):
        if len(p) == 6:
            diff = get_diff(one, p)
            if len(diff) == 1:
                solved[6] = p
                remaining_patterns += patterns[i + 1:]
                return (remaining_patterns, solved)

        remaining_patterns.append(p)

    return (remaining_patterns, solved)


def solve_five(patterns, solved):
    remaining_patterns = []
    six = solved[6]
    for i, p in enumerate(patterns):
        if len(p) == 5:
            diff = get_diff(six, p)
            if len(diff) == 1:
                solved[5] = p
                remaining_patterns += patterns[i + 1:]
                return (remaining_patterns, solved)

        remaining_patterns.append(p)

    return (remaining_patterns, solved)


def solve_nine_and_zero(patterns, solved):
    remaining_patterns = []
    five = solved[5]
    for p in patterns:
        if len(p) == 6:
            diff = get_diff(p, five)
            if len(diff) == 1:
                solved[9] = p
            else:
                solved[0] = p
        remaining_patterns.append(p)

    return (remaining_patterns, solved)


def solve_two_and_three(patterns, solved):
    remaining_patterns = []
    one = solved[1]
    for p in patterns:
        if len(p) == 5:
            diff = get_diff(one, p)
            if len(diff) == 1:
                solved[2] = p
            else:
                solved[3] = p

    return (remaining_patterns, solved)


value_sum = 0
for p in pairs:
    solved = [None] * 10
    remaining, solved = solve_known_digits(p['patterns'], solved)
    remaining, solved = solve_six(remaining, solved)
    remaining, solved = solve_five(remaining, solved)
    remaining, solved = solve_nine_and_zero(remaining, solved)
    remaining, solved = solve_two_and_three(remaining, solved)

    value = ''
    for d in p['digits']:
        for i, s in enumerate(solved):
            digit = list(d)
            solved_digit = list(s)
            digit.sort()
            solved_digit.sort()
            if digit == solved_digit:
                value += str(i)
                break
    value_sum += int(value)


print(value_sum)
