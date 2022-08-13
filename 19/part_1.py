from copy import deepcopy
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

Location = Tuple[int, int]
Offset = TypedDict('Offset', {'x': int, 'y': int})


class Beacon:
    def __init__(self, location: Location) -> None:
        self.x, self.y = location

    def get_location(self) -> Location:
        return (self.x, self.y)

    def set_location(self, location: Location) -> None:
        self.x, self.y = location


BeaconList = List[Beacon]


class Scanner:
    def __init__(self, id: str, beacons: BeaconList = []) -> None:
        self.id = id
        self.beacons = beacons
        self.location = None

    def set_location(self, location: Location):
        self.location = location


ScannerList = List[Scanner]


def setup() -> ScannerList:
    scanners = []
    for i, sd in enumerate(scanner_data):
        beacon_list = []
        for b in sd:
            beacon_list.append(Beacon(b))
        scanner = Scanner(id=str(i), beacons=beacon_list)
        scanners.append(scanner)
    return scanners


def calc_offset(beacon_1: Beacon, beacon_2: Beacon) -> Offset:
    return {
        'x': beacon_1.x - beacon_2.x,
        'y': beacon_1.y - beacon_2.y
    }


def check_overlap(scanner_1: Scanner, scanner_2: Scanner, offset: Offset) -> Tuple[bool, BeaconList]:
    OVERLAP_THRESHOLD = 3
    offset_beacons: BeaconList = [Beacon((b.x + offset['x'], b.y + offset['y']))
                                  for b in scanner_2.beacons]
    overlapping_beacon_locations: List[Location] = set([b.get_location() for b in scanner_1.beacons]).intersection(
        b.get_location() for b in offset_beacons)
    unique_beacon_locations = set([b.get_location() for b in scanner_1.beacons]).symmetric_difference(
        b.get_location() for b in offset_beacons)
    return (len(overlapping_beacon_locations) >= OVERLAP_THRESHOLD, [Beacon(l) for l in unique_beacon_locations])


scanners = setup()

current_scanner = scanners[0]
master_scanner = Scanner(
    id='master', beacons=deepcopy(current_scanner.beacons))
for scanner in scanners[1:]:
    for current_beacon in current_scanner.beacons:
        for beacon in scanner.beacons:
            offset = calc_offset(beacon_1=current_beacon, beacon_2=beacon)
            overlap_result = check_overlap(current_scanner, scanner, offset)

            if overlap_result[0]:
                scanner.set_location((offset['x'], offset['y']))
                master_scanner.beacons = master_scanner.beacons + \
                    overlap_result[1]
                break

print(len(master_scanner.beacons))
