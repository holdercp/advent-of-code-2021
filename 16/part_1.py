packet_bin = ''
with open('16/input.txt') as f:
    transmission = f.read().strip()
    bytes = bytes.fromhex(transmission)
    packet = int.from_bytes(bytes, 'big')
    packet = bin(packet)[2:]


def split_packet(packet):
    header = packet[:6]
    body = packet[6:]
    return (header, body)


def decode_header(header):
    version = header[:3]
    type_id = header[3:]

    return (int(version, 2), int(type_id, 2))


def get_value(body):


literal_value_type = 4

header, body = split_packet(packet)
version, type_id = decode_header(header)

if type_id == literal_value_type:
    value = get_value(body)

print(version, type_id)
