heightmap = []
with open('09/input.txt') as f:
    heightmap = f.read().strip().splitlines()
    heightmap = [list(hm) for hm in heightmap]
    for row in heightmap:
        for i, digit in enumerate(row):
            row[i] = int(digit)


def get_neighbors(coordinates, heightmap):
    col_cur, row_cur = coordinates
    neighbors = []
    row_prev = row_cur-1
    row_next = row_cur+1
    col_prev = col_cur-1
    col_next = col_cur+1
    has_prev_row = row_prev >= 0
    has_next_row = row_next < len(heightmap)
    has_prev_col = col_prev >= 0
    has_next_col = col_next < len(row)

    if has_prev_row:
        neighbors.append(heightmap[row_prev][col_cur])
    if has_next_col:
        neighbors.append(heightmap[row_cur][col_next])
    if has_next_row:
        neighbors.append(heightmap[row_next][col_cur])
    if has_prev_col:
        neighbors.append(heightmap[row_cur][col_prev])

    return neighbors


low_points = []
for row_cur, row in enumerate(heightmap):
    for col_cur, level in enumerate(row):
        neighbors = get_neighbors(coordinates=(
            col_cur, row_cur), heightmap=heightmap)

        if min(neighbors) > level:
            low_points.append(level)

print(sum(low_points) + len(low_points))
