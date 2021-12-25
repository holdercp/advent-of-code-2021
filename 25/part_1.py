map = {}
easterners = set()
southerners = set()
with open('25/input.txt') as f:
    grid = f.read().strip().splitlines()
    grid = [list(row) for row in grid]
    for y, row in enumerate(grid):
        for x, loc in enumerate(row):
            coordinates = (x, y)
            map[coordinates] = 0 if loc == '.' else 1

            if loc == '>':
                easterners.add(coordinates)
            if loc == 'v':
                southerners.add(coordinates)


grid_height = len(grid)
grid_width = len(grid[0])
has_moves = True
steps = 0
while has_moves:
    steps += 1

    move_east = []
    for cucumber in easterners:
        x, y = cucumber
        next_loc = ((x + 1) % grid_width, y)
        if not map[next_loc]:
            move_east.append((cucumber, next_loc))
    for movement in move_east:
        current, destination = movement
        map[current] = 0
        map[destination] = 1
        easterners.remove(current)
        easterners.add(destination)

    move_south = []
    for cucumber in southerners:
        x, y = cucumber
        next_loc = (x, (y + 1) % grid_height)
        if not map[next_loc]:
            move_south.append((cucumber, next_loc))
    for movement in move_south:
        current, destination = movement
        map[current] = 0
        map[destination] = 1
        southerners.remove(current)
        southerners.add(destination)

    if len(move_east) == 0 == len(move_south):
        has_moves = False

print(steps)
