line_coordinates = []
with open("05/input.txt") as f:
    lines = f.read().splitlines()
    lines = [l.split(' -> ') for l in lines]
    for i, line in enumerate(lines):
        for j, segment in enumerate(line):
            coordinates = segment.split(',')
            lines[i][j] = tuple([int(c) for c in coordinates])


def destructure_segment(segment):
    start, end = segment
    x_1, y_1 = start
    x_2, y_2 = end
    return (x_1, y_1, x_2, y_2)


def get_segment_directions(segment):
    x_1, y_1, x_2, y_2 = destructure_segment(segment)
    x_dir = y_dir = 'none'

    if x_1 < x_2:
        x_dir = 'forward'
    if x_1 > x_2:
        x_dir = 'reverse'

    if y_1 < y_2:
        y_dir = 'forward'
    if y_1 > y_2:
        y_dir = 'reverse'

    return (x_dir, y_dir)


def cover_point(diagram, coordinate):
    x, y = coordinate
    if y in diagram:
        if x in diagram[y]:
            diagram[y][x] += 1
        else:
            diagram[y][x] = 1
    else:
        diagram[y] = {}
        diagram[y][x] = 1


def trace_segment(diagram, segment):
    x_1, y_1, x_2, y_2 = destructure_segment(segment)

    if x_1 == x_2 or y_1 == y_2:
        x_dir, y_dir = get_segment_directions(segment)
        current_coordinate = [x_1, y_1]

        cover_point(diagram, current_coordinate)
        while current_coordinate[0] != x_2 or current_coordinate[1] != y_2:
            if x_dir == 'forward':
                current_coordinate[0] += 1
            elif x_dir == 'reverse':
                current_coordinate[0] -= 1

            if y_dir == 'forward':
                current_coordinate[1] += 1
            elif y_dir == 'reverse':
                current_coordinate[1] -= 1

            cover_point(diagram, current_coordinate)


diagram = {}
for segment in lines:
    trace_segment(diagram, segment)

overlaps = 0
for row in diagram.values():
    for p in row.values():
        if p >= 2:
            overlaps += 1

print(overlaps)
