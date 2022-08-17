from typing import List, Tuple, TypedDict
import queue

scanner_data = []
with open('19/input.txt') as f:
    scanner_data_raw = f.read().strip().split('\n\n')
    scanner_data_raw = [d.splitlines() for d in scanner_data_raw]
    for sdr in scanner_data_raw:
        coordinates = sdr[1:]
        beacons = []
        for coords in coordinates:
            beacons.append(tuple([int(coor)
                                  for coor in coords.split(",")]))
        scanner_data.append(beacons)

Beacon = Tuple[int, int, int]
BeaconList = List[Beacon]
Scanner = TypedDict(
    'Scanner', {'id': str, 'beacons': BeaconList, 'rotations': List[BeaconList]})
ScannerList = List[Scanner]

OVERLAP_THRESHOLD = 12

rotate_functions = [
    # positive x
    lambda coord: (+coord[0], +coord[1], +coord[2]),
    lambda coord: (+coord[0], -coord[2], +coord[1]),
    lambda coord: (+coord[0], -coord[1], -coord[2]),
    lambda coord: (+coord[0], +coord[2], -coord[1]),
    # negative x
    lambda coord: (-coord[0], -coord[1], +coord[2]),
    lambda coord: (-coord[0], +coord[2], +coord[1]),
    lambda coord: (-coord[0], +coord[1], -coord[2]),
    lambda coord: (-coord[0], -coord[2], -coord[1]),
    # positive y
    lambda coord: (+coord[1], +coord[2], +coord[0]),
    lambda coord: (+coord[1], -coord[0], +coord[2]),
    lambda coord: (+coord[1], -coord[2], -coord[0]),
    lambda coord: (+coord[1], +coord[0], -coord[2]),
    # negative y
    lambda coord: (-coord[1], -coord[2], +coord[0]),
    lambda coord: (-coord[1], +coord[0], +coord[2]),
    lambda coord: (-coord[1], +coord[2], -coord[0]),
    lambda coord: (-coord[1], -coord[0], -coord[2]),
    # positive z
    lambda coord: (+coord[2], +coord[0], +coord[1]),
    lambda coord: (+coord[2], -coord[1], +coord[0]),
    lambda coord: (+coord[2], -coord[0], -coord[1]),
    lambda coord: (+coord[2], +coord[1], -coord[0]),
    # negative z
    lambda coord: (-coord[2], -coord[0], +coord[1]),
    lambda coord: (-coord[2], +coord[1], +coord[0]),
    lambda coord: (-coord[2], +coord[0], -coord[1]),
    lambda coord: (-coord[2], -coord[1], -coord[0]),
]


def setup_scanners() -> ScannerList:
    scanners = []
    for i, sd in enumerate(scanner_data):
        scanner = {'id': str(i), 'beacons': [b for b in sd], 'rotations': []}
        for rotate in rotate_functions:
            rotation = [rotate(b) for b in scanner['beacons']]
            scanner['rotations'].append(rotation)
        scanners.append(scanner)
    return scanners


def calc_offset(beacon_1: Beacon, beacon_2: Beacon) -> Beacon:
    return (beacon_1[0] - beacon_2[0], beacon_1[1] - beacon_2[1], beacon_1[2] - beacon_2[2])


def check_overlap(beacons_1: BeaconList, beacons_2: BeaconList, offset: Beacon) -> Tuple[bool, BeaconList]:
    offset_beacons: BeaconList = [
        (b[0] + offset[0], b[1] + offset[1], b[2] + offset[2]) for b in beacons_2]
    overlapping_beacons: List[Beacon] = set(
        beacons_1).intersection(offset_beacons)

    return (len(overlapping_beacons) >= OVERLAP_THRESHOLD, offset_beacons)


def compare_beacons(beacons: BeaconList, rotations: List[BeaconList]) -> BeaconList:
    for beacon in beacons:
        for rotation in rotations:
            for rotated_beacon in rotation:
                offset = calc_offset(beacon, rotated_beacon)
                does_overlap, offset_beacons = check_overlap(
                    beacons, rotation, offset)

                if does_overlap:
                    return offset_beacons
    return []


def search_overlap(located_scanner: Scanner, unknown_scanners: ScannerList) -> ScannerList:
    overlapping_scanners = []
    for u_scanner in unknown_scanners:
        if u_scanner == located_scanner:
            continue
        offset_beacons = compare_beacons(
            located_scanner['beacons'], u_scanner['rotations'])
        if len(offset_beacons) > 0:
            print(
                f'      Found overlap with scanner {u_scanner["id"]}')
            u_scanner['beacons'] = offset_beacons
            overlapping_scanners.append(u_scanner)

    return overlapping_scanners


scanners = setup_scanners()
beacons = set(scanners[0]['beacons'])
located_scanners: ScannerList = queue.Queue()
located_scanners.put(scanners[0])
seen_scanners: str = []

while not located_scanners.empty():
    located_scanner: Scanner = located_scanners.get()
    seen_scanners.append(located_scanner['id'])

    print(f'Searching for overlaps with scanner {located_scanner["id"]}...')
    overlapping_scanners = search_overlap(located_scanner, scanners)

    if len(overlapping_scanners) == 0:
        print(f'WARN: No overlaps found for scanner {located_scanner["id"]}!')
    else:
        for o_scanner in overlapping_scanners:
            beacons |= set(o_scanner['beacons'])
            if o_scanner['id'] not in seen_scanners:
                located_scanners.put(o_scanner)

print(len(beacons))
