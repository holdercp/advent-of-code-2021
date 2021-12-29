reboot_steps = []
with open('22/input.txt') as f:
    steps = f.read().strip().splitlines()
    for s in steps:
        step = {}

        command, ranges = s.split(' ')
        ranges = ranges.split(',')
        for r in ranges:
            coordinate, rng = r.split('=')
            start, end = rng.split('..')

            if int(start) < -50 or 50 < int(end):
                break

            step[coordinate] = {}
            step[coordinate] = range(int(start), int(end) + 1)

        if step:
            step['command'] = command
            reboot_steps.append(step)

on = set()

for s in reboot_steps:

    for z in s['z']:
        for y in s['y']:
            for x in s['x']:
                cuboid = (x, y, z)
                if s['command'] == 'on':
                    on.add(cuboid)
                elif cuboid in on:
                    on.remove(cuboid)


print(len(on))
