template = ''
rules = []
with open('14/input.txt') as f:
    template, rules = f.read().strip().split('\n\n')

    rules = rules.splitlines()
    for i, r in enumerate(rules):
        rules[i] = tuple(r.split(' -> '))


def init_pairs(template):
    poly_count = {}
    pairs = {}
    for i, char in enumerate(template):
        poly_count[char] = 1 if char not in poly_count else poly_count[char] + 1
        if i == 0:
            continue

        pair_key = template[i-1] + char
        pairs[pair_key] = 1 if pair_key not in pairs else pairs[pair_key] + 1

    return (pairs, poly_count)


def get_updates(pairs, rule):
    key, insert = rule
    if key in pairs and pairs[key] > 0:
        left = key[0]
        right = key[1]
        num = pairs[key]
        left_pair = left + insert
        right_pair = insert + right

        if insert in poly_count:
            poly_count[insert] += num
        else:
            poly_count[insert] = num

        if left_pair in updates:
            updates[left_pair] += num
        else:
            updates[left_pair] = num

        if right_pair in updates:
            updates[right_pair] += num
        else:
            updates[right_pair] = num

        if key in updates:
            updates[key] -= num
        else:
            updates[key] = -num

    return updates


steps = 40
pairs, poly_count = init_pairs(template)
for s in range(steps):
    updates = {}
    for rule in rules:
        updates = get_updates(pairs, rule)
    for key, update in updates.items():
        if key in pairs:
            pairs[key] += update
        else:
            pairs[key] = update
most = max(poly_count.values())
least = min(poly_count.values())

print(most - least)
