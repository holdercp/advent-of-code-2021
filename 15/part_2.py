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

    unvisited_neighbors = unvisited.intersection(neighbors)

    return unvisited_neighbors


def calc_risk(node, nodes):
    lowest = None
    for n in nodes:
        risk_level = lowest_risk_paths[node] + risk_levels[n]

        if risk_level < lowest_risk_paths[n]:
            lowest_risk_paths[n] = risk_level

        if lowest != None:
            if risk_level < lowest_risk_paths[lowest]:
                lowest = n
        else:
            lowest = n
    unvisited.remove(node)

    return lowest


def get_next_node(paths, unvisited):
    tentative_paths = [(p, l) for p, l in paths.items()
                       if l < float('inf') and p in unvisited]
    next = min(tentative_paths, key=lambda n: n[1])
    return next[0]


unvisited = set()
lowest_risk_paths = {}
for node in risk_levels.keys():
    unvisited.add(node)
    lowest_risk_paths[node] = float('inf')

initial = (0, 0)
destination = (499, 499)
lowest_risk_paths[initial] = 0
current = initial
while len(unvisited) > 0:
    unvisited_neighbors = get_unvisited_neighbors(current)
    calc_risk(current, unvisited_neighbors)
    next_node = get_next_node(lowest_risk_paths, unvisited)

    if next_node == destination:
        break

    current = next_node

print(lowest_risk_paths[destination])
