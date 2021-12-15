risk_levels = {}
grid_height = 0
grid_width = 0
with open('15/input.txt') as f:
    grid = f.read().strip().splitlines()
    grid = [list(row) for row in grid]
    grid_height = len(grid)
    grid_width = len(grid[0])
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            location = (x, y)
            risk_levels[location] = int(level)


def get_neighbors(path):
    neighbors = {}
    for node in path:
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
            location = (x, y_prev)
            if location not in neighbors:
                neighbors[location] = []
            neighbors[location].append(
                risk[node] + risk_levels[location])
        if has_next_col:
            location = (x_next, y)
            if location not in neighbors:
                neighbors[location] = []
            neighbors[location].append(risk[node] + risk_levels[location])
        if has_next_row:
            location = (x, y_next)
            if location not in neighbors:
                neighbors[location] = []
            neighbors[location].append(risk[node] + risk_levels[location])
        if has_prev_col:
            location = (x_prev, y)
            if location not in neighbors:
                neighbors[location] = []
            neighbors[location].append(risk[node] + risk_levels[location])

    return neighbors


unvisited = set()
risk = {}
for location in risk_levels.keys():
    unvisited.add(location)
    risk[location] = None

initial = (0, 0)
unvisited.remove(initial)
risk[initial] = 0
path = [initial]
while len(unvisited) > 0:
    neighbors = get_neighbors(path)
    unvisited_neighbors = [(n, risk)
                           for n, risk in neighbors.items() if n in unvisited]

    lowest = ()
    for n in unvisited_neighbors:
        location = n[0]
        lowest_risk = min(n[1])
        risk[location] = lowest_risk
        if not lowest:
            lowest = (location, lowest_risk)
        elif lowest_risk < lowest[1]:
            lowest = (location, lowest_risk)
    unvisited.remove(lowest[0])
    path.append(lowest[0])

print(risk[(99, 99)])
