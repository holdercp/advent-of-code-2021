depths = []
with open("01/input.txt") as f:
    depths = f.read().splitlines()
depths = [int(d) for d in depths]

increases = 0
prev = None
for i, d in enumerate(depths):
    if i > 0 and d > prev:
        increases += 1
    prev = d

print(increases)
