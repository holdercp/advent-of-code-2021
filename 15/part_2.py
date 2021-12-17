def increment_grid(grid):
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            grid[y][x] = int(level) + 1 if int(level) < 9 else 1
    return grid


risk_levels = {}
grid_height = 0
grid_width = 0
with open('15/input.txt') as f:
    grid = f.read().strip().splitlines()
    grid = [list(row) for row in grid]

    for i in range(len(grid) * 4):
        row = grid[i]
        incremented_row = [int(l) + 1 if int(l) < 9 else 1 for l in row]
        grid.append(incremented_row)

    for row in grid:
        for i in range(len(row) * 4):
            row.append(int(row[i]) + 1 if int(row[i]) < 9 else 1)

    grid_height = len(grid)
    grid_width = len(grid[0])
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            location = (x, y)
            risk_levels[location] = int(level)


def get_unvisited_neighbors(node):
    neighbors = set()
    x, y = node

    y_prev = y-1
    y_next = y+1
    x_prev = x-1
    x_next = x+1
    has_prev_row = y_prev >= 0
    has_next_row = y_next < grid_height
    has_prev_col = x_prev >= 0
    has_next_col = x_next < grid_width

    if has_prev_row:
        node_key = (x, y_prev)
        neighbors.add(node_key)
    if has_next_col:
        node_key = (x_next, y)
        neighbors.add(node_key)
    if has_next_row:
        node_key = (x, y_next)
        neighbors.add(node_key)
    if has_prev_col:
        node_key = (x_prev, y)
        neighbors.add(node_key)

    unvisited_neighbors = neighbors.difference(visited)

    return unvisited_neighbors


def get_min_node():
    unvisited = {node: level for node,
                 level in risks.items() if node not in visited}
    return min(unvisited, key=unvisited.get)


visited = set()
risks = {}
initial = (0, 0)
destination = (499, 499)

risks[initial] = 0
while len(visited) < len(risk_levels):
    current = get_min_node()
    visited.add(current)

    if current == destination:
        break

    neighbors = get_unvisited_neighbors(current)
    for neighbor in neighbors:
        level = risks[current] + risk_levels[neighbor]
        if neighbor in risks:
            if level < risks[neighbor]:
                risks[neighbor] = level
        else:
            risks[neighbor] = level


print(risks[destination])
