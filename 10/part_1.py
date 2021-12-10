chunks = []
with open('10/input.txt') as f:
    chunks = f.read().strip().splitlines()

closers = [')', ']', '}', '>']
matches = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def check(chunk):
    stack = []

    for token in chunk:
        if token in closers:
            last_opener = stack.pop()
            match = matches[last_opener]
            if match != token:
                raise Exception(
                    f'Expected {match}, but found {token} instead.', token)
        else:
            stack.append(token)


score = 0
for c in chunks:
    try:
        check(c)
    except Exception as e:
        bad_match = e.args[1]
        score += points[bad_match]

print(score)
