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

Location = Tuple[int, int]


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


scanners = setup()
