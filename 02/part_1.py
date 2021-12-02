commands = []
with open("02/input.txt") as f:
    commandsRaw = f.read().splitlines()
    for c in commandsRaw:
        cTuple = c.split(" ")
        cTuple[1] = int(cTuple[1])
        cTuple = tuple(cTuple)
        commands.append(cTuple)

sub = {
    'depth': 0,
    'position': 0
}

for c in commands:
    instruction = c[0]
    value = c[1]
    if instruction == 'forward':
        sub['position'] += value
    elif instruction == 'up':
        sub['depth'] -= value
    elif instruction == 'down':
        sub['depth'] += value

print(sub['position'] * sub['depth'])
