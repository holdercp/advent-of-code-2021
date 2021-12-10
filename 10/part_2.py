import statistics

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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
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


def remove_corrupted(chunks):
    for c in chunks.copy():
        try:
            check(c)
        except Exception:
            chunks.remove(c)
    return chunks


def complete(chunk):
    stack = []
    added = []
    for token in chunk:
        if token in closers:
            stack.pop()
        else:
            stack.append(token)

    for opener in reversed(stack):
        added.append(matches[opener])

    return added


incomplete = remove_corrupted(chunks=chunks)
totals = []
for chunk in incomplete:
    score = 0
    added = complete(chunk=chunk)
    for closer in added:
        score = (score * 5) + points[closer]
    totals.append(score)


print(statistics.median(totals))
