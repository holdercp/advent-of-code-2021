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
    # TODO: Complete implementation
    # If intersects, return coordinates of intersection
    # Else return None
    return None


kept_cuboids = []
for c in cuboids:
    if c.type == 1:
        kept_cuboids.append(c)

    for kc in kept_cuboids:
        intersection = get_intersection(c, kc)
        if (intersection):
            cuboid = Cuboid(coordinates=intersection, type=kc.type * -1)
            kept_cuboids.append(cuboid)

on_volume = 0
for c in kept_cuboids:
    on_volume += c.get_volume()
print(on_volume)
