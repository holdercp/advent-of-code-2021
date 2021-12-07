import math

fish = []
with open("06/input.txt") as f:
    fish = f.read().strip().split(',')
    fish = [int(f) for f in fish]

days = 256

school = [0] * 9
for f in fish:
    school[f] += 1

for d in range(days):
    new_fish = reset_fish = school.pop(0)
    school.append(new_fish)
    school[6] += reset_fish

print(sum(school))
