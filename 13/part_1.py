dots = []
instructions = []
with open('13/input.txt') as f:
    dots, instructions = f.read().strip().split('\n\n')

    dots = dots.splitlines()
    dots = [d.split(',') for d in dots]
    for i, dot in enumerate(dots):
        dots[i] = [int(d) for d in dot]

    instructions = instructions.splitlines()
    instructions = [i.split('fold along ', 1) for i in instructions]
    for i, instruction in enumerate(instructions):
        instructions[i] = instruction[1].split('=')
        instructions[i][1] = int(instructions[i][1])

axis, fulcrum = instructions[0]
counts = set()
for i, d in enumerate(dots):
    x, y = d
    if axis == 'x':
        if x > fulcrum:
            dots[i][0] -= (x - fulcrum) * 2
        counts.add(tuple(d))
    else:
        if y > fulcrum:
            dots[i][1] -= (y - fulcrum) * 2
        counts.add(tuple(d))
print(len(counts))
