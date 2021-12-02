depths = []
with open("01/input.txt") as f:
    depths = f.read().splitlines()
depths = [int(d) for d in depths]

windowSize = 3
increases = 0
sum = 0
for i, d in enumerate(depths):
    if i < windowSize:
        sum += d
    else:
        nextSum = sum - depths[i-windowSize] + d
        if sum < nextSum:
            increases += 1
        sum = nextSum

print(increases)
