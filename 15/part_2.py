import heapq


def increment_grid(grid):
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            grid[y][x] = int(level) + 1 if int(level) < 9 else 1
    return grid


def create_grid(file):
    grid = file.read().strip().splitlines()
    grid = [list(row) for row in grid]

    for i in range(len(grid) * 4):
        row = grid[i]
        incremented_row = [int(l) + 1 if int(l) < 9 else 1 for l in row]
        grid.append(incremented_row)

    for row in grid:
        for i in range(len(row) * 4):
            row.append(int(row[i]) + 1 if int(row[i]) < 9 else 1)

    return grid


def get_neighbors(node, grid):
    grid_height = len(grid)
    grid_width = len(grid[0])

    neighbors = {}
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
        vertex = (x, y_prev)
        neighbors[vertex] = int(grid[y_prev][x])
    if has_next_col:
        vertex = (x_next, y)
        neighbors[vertex] = int(grid[y][x_next])
    if has_next_row:
        vertex = (x, y_next)
        neighbors[vertex] = int(grid[y_next][x])
    if has_prev_col:
        vertex = (x_prev, y)
        neighbors[vertex] = int(grid[y][x_prev])

    return neighbors


def create_graph(grid):
    graph = {}
    for y, row in enumerate(grid):
        for x, level in enumerate(row):
            vertex = (x, y)
            neighbors = get_neighbors(vertex, grid)
            graph[vertex] = neighbors
    return graph


def calc_risk(graph, initial_vertex):
    levels = {vertex: float('inf') for vertex in graph}
    levels[initial_vertex] = 0
    pq = [(0, initial_vertex)]

    while len(pq) > 0:
        current_level, current_vertex = heapq.heappop(pq)

        if current_level > levels[current_vertex]:
            continue

        for neighbor, level in graph[current_vertex].items():
            level = current_level + level

            if level < levels[neighbor]:
                levels[neighbor] = level
                heapq.heappush(pq, (level, neighbor))

    return levels


levels_graph = {}
initial = (0, 0)
target = (499, 499)
with open('15/input.txt') as f:
    grid = create_grid(f)
    levels_graph = create_graph(grid)

risk = calc_risk(levels_graph, initial)

print(risk[target])
