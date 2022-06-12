from typing import NewType, Tuple, Union, Literal, TypedDict

coordinate_range = NewType('CoordinateRange', Tuple[int, int])
coordinates = TypedDict(
    'Coordinates', {'x': coordinate_range, 'y': coordinate_range, 'z': coordinate_range})


class Cuboid:
    def __init__(self, coordinates: coordinates, type: Literal[-1, 1]):
        self.coordinates = coordinates
        self.x = coordinates['x']
        self.y = coordinates['y']
        self.z = coordinates['z']
        self.type = type

    def get_volume(self) -> int:
        return (abs(self.x[0] - self.x[1]) * abs(self.y[0] - self.y[1]) * abs(self.z[0] - self.z[1])) * self.type


cuboids = []
with open('22/input.txt') as f:
    steps = f.read().strip().splitlines()
    for s in steps:
        step = {'coordinates': {}}

        command, ranges = s.split(' ')
        ranges = ranges.split(',')
        for r in ranges:
            plane, rng = r.split('=')
            start, end = rng.split('..')

            step['coordinates'][plane] = (int(start), int(end))

        step['type'] = 1 if command == 'on' else -1

        cuboid = Cuboid(step['coordinates'], step['type'])

        cuboids.append(cuboid)


def get_intersection(c1: Cuboid, c2: Cuboid) -> Union[coordinates, None]:
    if ((c1.x[0] > c2.x[1] or c1.x[1] < c2.x[0]) or (c1.y[0] > c2.y[1] or c1.y[1] < c2.y[0]) or (c1.z[0] > c2.z[1] or c1.z[1] < c2.z[0])):
        return None
    else:
        # TODO: Calculate intersection coordinates
        return {'x': (0, 0), 'y': (0, 0), 'z': (0, 0)}


kept_cuboids = []
for c in cuboids:
    cuboids_to_keep = []

    if c.type == 1:
        cuboids_to_keep.append(c)

    for kc in kept_cuboids:
        intersection = get_intersection(c, kc)
        if (intersection):
            cuboid = Cuboid(coordinates=intersection, type=kc.type * -1)
            cuboids_to_keep.append(cuboid)

    kept_cuboids += cuboids_to_keep


on_volume = 0
for c in kept_cuboids:
    on_volume += c.get_volume()
print(on_volume)
