outputs = []
with open("08/input.txt") as f:
    signals_and_outputs = f.read().strip().splitlines()
    for so in signals_and_outputs:
        signals, outputs_raw = so.split(' | ')
        outputs.extend(outputs_raw.split())

count = 0
for o in outputs:
    length = len(o)
    if 1 < length < 5 or length == 7:
        count += 1

print(count)
