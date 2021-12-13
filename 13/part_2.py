dots = []
instructions = []
with open('13/input.txt') as f:
    dots, instructions = f.read().strip().split('\n\n')

    dots = dots.splitlines()
    dots = [d.split(',') for d in dots]
    for i, dot in enumerate(dots):
        dots[i] = tuple([int(d) for d in dot])

    instructions = instructions.splitlines()
    instructions = [i.split('fold along ', 1) for i in instructions]
    for i, instruction in enumerate(instructions):
        instructions[i] = instruction[1].split('=')
        instructions[i][1] = int(instructions[i][1])

for instruction in instructions:
    axis, fulcrum = instruction

    for i, d in enumerate(dots):
        dList = list(d)
        x, y = dList
        if axis == 'x':
            if x > fulcrum:
                dList[0] -= (x - fulcrum) * 2
                dots[i] = tuple(dList)
        else:
            if y > fulcrum:
                dList[1] -= (y - fulcrum) * 2
                dots[i] = tuple(dList)
    dots = list(set(dots))

max_x = max([loc[0] for loc in dots])
max_y = max([loc[1] for loc in dots])
blank = ['.' for _ in range(max_x + 1)]
image = [blank.copy() for _ in range(max_y + 1)]
for d in dots:
    x, y = d
    image[y][x] = '#'

print(image)
