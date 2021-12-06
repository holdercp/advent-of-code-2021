import math

fish = []
with open("06/input.txt") as f:
    fish = f.read().strip().split(',')
    fish = [int(f) for f in fish]

days = 256
days_to_spawn_new = 9
days_to_spawn = 7
spawn = len(fish)


def sum_spawn(fish, days):
    days_remaining = days
    day_offset = days_to_spawn - (fish)
    spawn_count = max(0, math.floor(
        (days_remaining + day_offset) / days_to_spawn))

    for i in range(spawn_count):
        days_remaining -= fish if i == 0 else days_to_spawn
        spawn_count += sum_spawn(days_to_spawn_new, days_remaining)

    return spawn_count


for f in fish:
    spawn += sum_spawn(f + 1, days)

print(spawn)
