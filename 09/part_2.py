heightmap = []
with open('09/input.txt') as f:
    heightmap = f.read().strip().splitlines()
    heightmap = [list(hm) for hm in heightmap]
    for row in heightmap:
        for i, digit in enumerate(row):
            row[i] = int(digit)

peak_level = 9


def get_neighbors(coordinates, heightmap):
    col_cur, row_cur = coordinates
    neighbors = {}
    row_prev = row_cur-1
    row_next = row_cur+1
    col_prev = col_cur-1
    col_next = col_cur+1
    has_prev_row = row_prev >= 0
    has_next_row = row_next < len(heightmap)
    has_prev_col = col_prev >= 0
    has_next_col = col_next < len(row)

    if has_prev_row:
        coordinates = (col_cur, row_prev)
        level = heightmap[row_prev][col_cur]
        neighbors[coordinates] = level
    if has_next_col:
        coordinates = (col_next, row_cur)
        level = heightmap[row_cur][col_next]
        neighbors[coordinates] = level
    if has_next_row:
        coordinates = (col_cur, row_next)
        level = heightmap[row_next][col_cur]
        neighbors[coordinates] = level
    if has_prev_col:
        coordinates = (col_prev, row_cur)
        level = heightmap[row_cur][col_prev]
        neighbors[coordinates] = level

    return neighbors


def find_low_points(heightmap):
    low_points = []
    for row_cur, row in enumerate(heightmap):
        for col_cur, level in enumerate(row):
            neighbors = get_neighbors(coordinates=(
                col_cur, row_cur), heightmap=heightmap)
            neighbor_levels = list(neighbors.values())

            if min(neighbor_levels) > level:
                low_points.append((col_cur, row_cur))
    return low_points


def trace_basin(basin, low_point, heightmap):
    basin.add(low_point)
    neighbors = get_neighbors(coordinates=low_point, heightmap=heightmap)
    for coordinates, level in neighbors.items():
        if level < peak_level and coordinates not in basin:
            basin = trace_basin(
                basin=basin, low_point=coordinates, heightmap=heightmap)
    return basin


low_points = find_low_points(heightmap=heightmap)
basins = []
for lp in low_points:
    basin = trace_basin(basin=set(), low_point=lp, heightmap=heightmap)
    basins.append(basin)
basins.sort(key=len, reverse=True)

print(len(basins[0]) * len(basins[1]) * len(basins[2]))
