from typing import List, Tuple

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

Coordinate = Tuple[int, int]
BeaconList = List[Coordinate]

OVERLAP_THRESHOLD = 3


class Scanner:
    def __init__(self, id: str, beacons: BeaconList = []) -> None:
        self.id = id
        self.beacons = beacons


ScannerList = List[Scanner]


def setup() -> ScannerList:
    scanners = []
    for i, sd in enumerate(scanner_data):
        scanner = Scanner(str(i), [b for b in sd])
        scanners.append(scanner)
    return scanners


def calc_offset(beacon_1: Coordinate, beacon_2: Coordinate) -> Coordinate:
    return (beacon_1[0] - beacon_2[0], beacon_1[1] - beacon_2[1])


def check_overlap(scanner_1: Scanner, scanner_2: Scanner, offset: Coordinate) -> Tuple[bool, BeaconList]:
    offset_beacons: BeaconList = [
        (b[0] + offset[0], b[1] + offset[1]) for b in scanner_2.beacons]
    overlapping_beacon_locations: List[Coordinate] = set(
        scanner_1.beacons).intersection(offset_beacons)

    return (len(overlapping_beacon_locations) >= OVERLAP_THRESHOLD, offset_beacons)


def search_overlap(origin_scanner: Scanner, scanners: ScannerList) -> Scanner:
    for scanner in scanners:
        for origin_beacon in origin_scanner.beacons:
            for beacon in scanner.beacons:
                offset = calc_offset(origin_beacon, beacon)
                does_overlap, offset_beacons = check_overlap(
                    origin_scanner, scanner, offset)

                if does_overlap:
                    scanner.beacons = offset_beacons
                    return scanner

    raise Exception(
        f'Overlap was not found with scanner: {origin_scanner.id}')


scanners = setup()
scanner = scanners.pop(0)
beacons = set(scanner.beacons)

while len(scanners) > 0:
    overlapping_scanner = search_overlap(scanner, scanners)
    beacons |= set(overlapping_scanner.beacons)
    scanner = scanners.pop(scanners.index(overlapping_scanner))


print(len(beacons))
print(beacons)
