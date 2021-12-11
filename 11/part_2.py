grid = []
with open('11/input.txt') as f:
    grid = f.read().strip().splitlines()
    grid = [list(row) for row in grid]
    for row in grid:
        for y, level in enumerate(row):
            row[y] = int(level)

first_flash = None


def increase_energy(grid):
    for row in grid:
        for x, level in enumerate(row):
            row[x] = level + 1
    return grid


def flash(location, grid, flashed):
    flashed.append(location)

    x, y = location
    col_start = x - 1 if x > 0 else 0
    col_end = x + 1 if x < len(grid[0]) - 1 else len(grid[0]) - 1
    row_start = y - 1 if y > 0 else 0
    row_end = y + 1 if y < len(grid) - 1 else len(grid) - 1

    for ny in range(row_start, row_end + 1):
        for nx in range(col_start, col_end + 1):
            if nx == x and ny == y:
                continue
            neighbor = (nx, ny)
            grid[ny][nx] += 1
            if grid[ny][nx] > 9 and neighbor not in flashed:
                grid = flash(location=neighbor, grid=grid, flashed=flashed)

    return grid


step = 1
while first_flash == None:
    flashed = []
    grid = increase_energy(grid=grid)
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            if level > 9 and (x, y) not in flashed:
                grid = flash(location=(x, y), grid=grid, flashed=flashed)
    if len(flashed) == 100:
        first_flash = step
        break
    for f in flashed:
        x, y = f
        grid[y][x] = 0
    step += 1

print(first_flash)
