from typing import List, Tuple, TypedDict

scanner_data = []
with open('19/input_2d.txt') as f:
    scanner_data_raw = f.read().strip().split('\n\n')
    scanner_data_raw = [d.splitlines() for d in scanner_data_raw]
    for sdr in scanner_data_raw:
        coordinates = sdr[1:]
        beacons = []
        for coords in coordinates:
            beacons.append(tuple([int(coor)
                                  for coor in coords.split(",")]))
        scanner_data.append(beacons)

Beacon = Tuple[int, int]
BeaconList = List[Beacon]
Scanner = TypedDict(
    'Scanner', {'beacons': BeaconList, 'rotations': List[BeaconList]})
ScannerList = List[Scanner]

OVERLAP_THRESHOLD = 3

rotate_functions = [
    lambda coor: coor,
    lambda coor: (-coor[1], -coor[0]),
    lambda coor: (-coor[0], -coor[1]),
    lambda coor: (-coor[1], coor[0]),
    lambda coor: (-coor[0], coor[1]),
    lambda coor: (coor[1], coor[0]),
    lambda coor: (coor[0], -coor[1]),
    lambda coor: (-coor[1], -coor[0]),
]


def setup() -> ScannerList:
    scanners = []
    for i, sd in enumerate(scanner_data):
        scanner = {'beacons': [b for b in sd], 'rotations': []}
        for rotate in rotate_functions:
            rotation = [rotate(b) for b in scanner['beacons']]
            scanner['rotations'].append(rotation)
        scanners.append(scanner)
    return scanners


def calc_offset(beacon_1: Beacon, beacon_2: Beacon) -> Beacon:
    return (beacon_1[0] - beacon_2[0], beacon_1[1] - beacon_2[1])


def check_overlap(beacons_1: BeaconList, beacons_2: BeaconList, offset: Beacon) -> Tuple[bool, BeaconList]:
    offset_beacons: BeaconList = [
        (b[0] + offset[0], b[1] + offset[1]) for b in beacons_2]
    overlapping_beacon_locations: List[Beacon] = set(
        beacons_1).intersection(offset_beacons)

    return (len(overlapping_beacon_locations) >= OVERLAP_THRESHOLD, offset_beacons)


def search_overlap(origin_scanner: Scanner, scanners: ScannerList) -> Scanner:
    for scanner in scanners:
        for origin_beacon in origin_scanner['beacons']:
            for rotation in scanner['rotations']:
                for beacon in rotation:
                    offset = calc_offset(origin_beacon, beacon)
                    does_overlap, offset_beacons = check_overlap(
                        origin_scanner['beacons'], rotation, offset)

                    if does_overlap:
                        scanner['beacons'] = offset_beacons
                        return scanner

    raise Exception(
        f'Overlap was not found with scanner: {origin_scanner.id}')


scanners = setup()
scanner = scanners.pop(0)
beacons = set(scanner['beacons'])

while len(scanners) > 0:
    overlapping_scanner = search_overlap(scanner, scanners)
    beacons |= set(overlapping_scanner['beacons'])
    scanner = scanners.pop(scanners.index(overlapping_scanner))


print(len(beacons))
print(beacons)
