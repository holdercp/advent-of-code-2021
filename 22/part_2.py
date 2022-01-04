reboot_steps = []
with open('22/input.txt') as f:
    steps = f.read().strip().splitlines()
    for s in steps:
        step = {}

        command, ranges = s.split(' ')
        ranges = ranges.split(',')
        for r in ranges:
            coordinate, rng = r.split('=')
            start, end = rng.split('..')

            step[coordinate] = {}
            step[coordinate] = (int(start), int(end))

        step['command'] = command
        reboot_steps.append(step)


def unpack_step(step):
    xr = step['x']
    yr = step['y']
    zr = step['z']
    cmd = step['command']

    return (xr, yr, zr, cmd)


def get_terminal_coordinates(x_range, y_range, z_range):
    x_min, x_max = x_range
    y_min, y_max = y_range
    z_min, z_max = z_range

    start = (x_min, y_min, z_min)
    end = (x_max, y_max, z_max)

    return (start, end)


def get_intersection(on_r, coordinate_r):
    on_min, on_max = on_r
    on_min_x, on_min_y, on_min_z = on_min
    on_max_x, on_max_y, on_max_z = on_max

    coordinate_min, coordinate_max = coordinate_r
    coordinate_min_x, coordinate_min_y, coordinate_min_z = coordinate_min
    coordinate_max_x, coordinate_max_y, coordinate_max_z = coordinate_max

    # Does not intersect
    if (on_min_x > coordinate_max_x and on_min_y > coordinate_max_y and on_min_z > coordinate_max_z) or (on_max_x < coordinate_min_x and on_max_y < coordinate_min_y and on_max_z < coordinate_min_z):
        return 'NONE'
    # Contains
    if (on_min_x <= coordinate_min_x and on_min_y <= coordinate_min_y and on_min_z <= coordinate_min_z) and (on_max_x >= coordinate_max_x and on_max_y >= coordinate_max_y and on_max_z >= coordinate_max_z):
        return 'CONTAINS'
    # Is contained
    if (on_min_x >= coordinate_min_x and on_min_y >= coordinate_min_y and on_min_z >= coordinate_min_z) and (on_max_x <= coordinate_max_x and on_max_y <= coordinate_max_y and on_max_z <= coordinate_max_z):
        return 'IS_CONTAINED'
    # Lower-bound intersection
    if (on_min_x > coordinate_min_x and on_min_y > coordinate_min_y and on_min_z > coordinate_min_z) and (on_max_x <= coordinate_max_x and on_max_y <= coordinate_max_y and on_max_z <= coordinate_max_z):
        return 'LOWER'
    # Upper-bound instersection

    return (on_min[0] <= coordinate_max[0] and on_max[0] >= coordinate_min[0]) and (on_min[1] <= coordinate_max[1] and on_max[1] >= coordinate_min[1]) and (on_min[2] <= coordinate_max[2] and on_max[2] >= coordinate_min[2])


on_ranges = []

first_step = reboot_steps.pop(0)
xr, yr, zr, cmd = unpack_step(first_step)
on_ranges.append(((xr[0], yr[0], zr[0]), (xr[1], yr[1], zr[1])))

for s in reboot_steps:
    xr, yr, zr, cmd = unpack_step(s)
    start, end = get_terminal_coordinates(xr, yr, zr)

    for on_range in on_ranges:
        intersection = get_intersection(on_range, (start, end))
        print()
