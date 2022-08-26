from enum import Enum
from typing import List, TypedDict


class ResultTypes(Enum):
    APPROACHING = 'approaching'
    LANDED = 'landed'
    OVERSHOT = 'overshot'


Coordinate = TypedDict('Coordinate', {'min': int, 'max': int})
Target = TypedDict('Target', {'x': Coordinate, 'y': Coordinate})

with open('17/input.txt') as f:
    target_raw = f.read().strip()
    x_start = target_raw.find("x=")
    x_sep = target_raw.find("..")
    y_start = target_raw.find("y=")
    y_sep = target_raw.rfind("..")

    target: Target = {
        'x': {
            'min': int(target_raw[x_start+2:x_sep]),
            'max': int(target_raw[x_sep+2:y_start-2])
        },
        'y': {
            'min': int(target_raw[y_start+2:y_sep]),
            'max': int(target_raw[y_sep+2:])
        }
    }


class Probe:
    def __init__(self, velocity: List[int]) -> None:
        self.x = 0
        self.y = 0
        self.velocity = velocity
        self.inital_velocity = tuple(velocity)

    def step(self) -> None:
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.reduce_velocity()

    def reduce_velocity(self) -> None:
        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        elif self.velocity[0] < 0:
            self.velocity[0] += 1

        self.velocity[1] -= 1


def check_probe(probe: Probe, target: Target) -> ResultTypes:
    if probe.x > target['x']['max'] or probe.y < target['y']['min']:
        return ResultTypes.OVERSHOT

    if probe.x >= target['x']['min'] and probe.x <= target['x']['max'] and probe.y <= target['y']['max'] and probe.y >= target['y']['min']:
        return ResultTypes.LANDED

    return ResultTypes.APPROACHING


valid_velocities = set()
for y in range(-1000, 1000):
    for x in range(target['x']['max'] + 1):
        traveling = True
        probe = Probe([x, y])

        while traveling:
            probe.step()
            result = check_probe(probe, target)

            if result == ResultTypes.OVERSHOT:
                traveling = False

            if result == ResultTypes.LANDED:
                valid_velocities.add(probe.inital_velocity)
                traveling = False

print(len(valid_velocities))
