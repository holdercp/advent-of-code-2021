commands = []
with open("02/input.txt") as f:
    commandsRaw = f.read().splitlines()
    for c in commandsRaw:
        cTuple = c.split(" ")
        cTuple[1] = int(cTuple[1])
        cTuple = tuple(cTuple)
        commands.append(cTuple)

print(commands)
