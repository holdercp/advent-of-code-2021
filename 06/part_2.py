import math

fish = []
with open("06/input.txt") as f:
    fish = f.read().strip().split(',')
    fish = [int(f) for f in fish]

days = 256


def generate_school(starting_fish):
    school = {}
    for n in range(9):
        school[n] = 0

    for f in starting_fish:
        school[f] += 1

    return school


def age_fish(school):
    new_fish = school[0]

    school[0] = school[1]
    school[1] = school[2]
    school[2] = school[3]
    school[3] = school[4]
    school[4] = school[5]
    school[5] = school[6]
    school[6] = school[7]
    school[7] = school[8]

    school[8] = new_fish
    school[6] += new_fish

    return school


school = generate_school(fish)
for d in range(days):
    school = age_fish(school.copy())

print(sum(school.values()))
