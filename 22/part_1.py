reboot_steps = []
with open('22/input.txt') as f:
    steps = f.read().strip().splitlines()
    for s in steps:
        step = {}
        command, ranges = s.split(' ')
        step['command'] = command

        ranges = ranges.split(',')
        for r in ranges:
            coordinate, rnge = r.split('=')
            start, end = rnge.split('..')

            step[coordinate] = {}
            step[coordinate] = range(int(start), int(end) + 1)

        reboot_steps.append(step)

print(reboot_steps)
