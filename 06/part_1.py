fish = []
with open("06/input.txt") as f:
    fish = f.read().strip().split(',')
    fish = [int(f) for f in fish]

days = 80
days_to_spawn_new = 8
days_to_spawn = 6

for d in range(days):
    for i, f in enumerate(fish.copy()):
        if f == 0:
            fish.append(days_to_spawn_new)
            fish[i] = days_to_spawn
        else:
            fish[i] -= 1

print(len(fish))
