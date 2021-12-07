subs = []
with open("07/input.txt") as f:
    subs = f.read().strip().split(',')
    subs = [int(s) for s in subs]


def calc_fuel(target, sub):
    diff = abs(sub - target)
    fuel_cost = int((diff * (diff + 1)) / 2)

    return fuel_cost


options = []
for pos in range(min(subs), max(subs) + 1):
    total_fuel = 0
    for s in subs:
        total_fuel += calc_fuel(target=pos, sub=s)
    options.append(total_fuel)

print(min(options))
