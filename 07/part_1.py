import statistics

subs = []
with open("07/input.txt") as f:
    subs = f.read().strip().split(',')
    subs = [int(s) for s in subs]

target = int(statistics.median(subs))

fuel_cost = 0
for s in subs:
    fuel_cost += abs(s - target)

print(fuel_cost)
