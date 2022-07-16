scanner_data = []
with open('19/input.txt') as f:
    scanner_data_raw = f.read().strip().split('\n\n')
    scanner_data_raw = [d.splitlines() for d in scanner_data_raw]
    for sdr in scanner_data_raw:
        coordinates = sdr[1:]
        for coords in coordinates:
            scanner_data.append(tuple([int(coor)
                                for coor in coords.split(",")]))


print(scanner_data)
