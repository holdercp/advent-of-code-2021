with open('17/input.txt') as f:
    target_raw = f.read().strip()
    x_start = target_raw.find("x=")
    x_sep = target_raw.find("..")
    y_start = target_raw.find("y=")
    y_sep = target_raw.rfind("..")

    target = {
        'x': {
            'min': int(target_raw[x_start+2:x_sep]),
            'max': int(target_raw[x_sep+2:y_start-2])
        },
        'y': {
            'min': int(target_raw[y_start+2:y_sep]),
            'max': int(target_raw[y_sep+2:])
        }
    }

print(target)
