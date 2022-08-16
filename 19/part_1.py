import re
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
OVERLAP_SUCCESS = 'overlap'
OVERLAP_FAILURE = 'no overlap'

rotate_functions = [
    lambda coor: coor,
    lambda coor: (-coor[1], coor[0], coor[2]),
    lambda coor: (-coor[0], -coor[1], coor[2]),
    lambda coor: (coor[1], -coor[0], coor[2]),
    lambda coor: (coor[2], coor[1], -coor[0]),
    lambda coor: (coor[2], coor[0], coor[1]),
    lambda coor: (coor[2], -coor[1], coor[0]),
    lambda coor: (coor[2], -coor[0], -coor[1]),
    lambda coor: (-coor[0], coor[1], -coor[2]),
    lambda coor: (-coor[1], coor[0], -coor[2]),
    lambda coor: (-coor[0], -coor[1], -coor[2]),
    lambda coor: (coor[1], -coor[0], -coor[2]),
    lambda coor: (-coor[2], coor[1], coor[0]),
    lambda coor: (-coor[2], coor[0], -coor[1]),
    lambda coor: (-coor[2], -coor[1], -coor[0]),
    lambda coor: (-coor[2], -coor[0], coor[1]),
    lambda coor: (coor[0], coor[2], -coor[1]),
    lambda coor: (-coor[1], coor[2], -coor[0]),
    lambda coor: (-coor[0], coor[2], coor[1]),
    lambda coor: (coor[1], coor[2], coor[0]),
    lambda coor: (coor[0], -coor[2], coor[1]),
    lambda coor: (coor[1], -coor[2], -coor[0]),
    lambda coor: (-coor[0], -coor[2], -coor[1]),
    lambda coor: (-coor[1], -coor[2], coor[0]),
]


def setup() -> ScannerList:
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


def compare_beacons(beacons: BeaconList, rotations: List[BeaconList]) -> Tuple[str, BeaconList]:
    for beacon in beacons:
        for rotation in rotations:
            for rotated_beacon in rotation:
                offset = calc_offset(beacon, rotated_beacon)
                does_overlap, offset_beacons = check_overlap(
                    beacons, rotation, offset)

                if does_overlap:
                    return (OVERLAP_SUCCESS, offset_beacons)
    return (OVERLAP_FAILURE, [])


def search_overlap(resolved_scanner: Scanner, scanners: ScannerList) -> List[Tuple[int, Scanner]]:
    overlapping_scanners = []
    for i, scanner in enumerate(scanners):
        if scanner == resolved_scanner:
            continue
        result, offset_beacons = compare_beacons(
            resolved_scanner['beacons'], scanner['rotations'])
        if result == OVERLAP_SUCCESS:
            print(
                f'      Found overlap with scanner {scanner["id"]}')
            scanner['beacons'] = offset_beacons
            overlapping_scanners.append((i, scanner))

    return overlapping_scanners


scanners = setup()
beacons = set(scanners[0]['beacons'])
resolved_scanners: ScannerList = queue.Queue()
resolved_scanners.put(scanners[0])
visited_scanners = []

while not resolved_scanners.empty():
    resolved_scanner = resolved_scanners.get()
    visited_scanners.append(resolved_scanner['id'])
    print(f'Searching for overlaps with scanner {resolved_scanner["id"]}...')
    overlapping_scanners = search_overlap(resolved_scanner, scanners)

    if len(overlapping_scanners) == 0:
        print(f'WARN: No overlaps found for scanner {resolved_scanner["id"]}!')
    else:
        for pos, os in overlapping_scanners:
            beacons |= set(os['beacons'])
            if os['id'] not in visited_scanners:
                resolved_scanners.put(os)

print(len(beacons))
