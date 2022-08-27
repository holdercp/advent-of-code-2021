hex_to_bin_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

with open('16/input.txt') as f:
    transmission = f.read().strip()
    packet = ''.join([hex_to_bin_map[c] for c in transmission])


def split_packet(packet):
    header = packet[:6]
    body = packet[6:]
    return (header, body)


def parse_header(header):
    version = header[:3]
    type_id = header[3:]

    return (int(version, 2), int(type_id, 2))


def get_literal_value(literal_value):
    value = ''
    group_start = 0
    group_end = 5
    bits_parsed = 0

    parsed = False
    while not parsed:
        group = literal_value[group_start+1:group_end]
        group_prefix = literal_value[group_start]

        value += group
        group_start += 5
        group_end += 5
        bits_parsed += 5

        if group_prefix == '0':
            parsed = True

    return (int(value, 2), bits_parsed)


def parse_body(body):
    length_type_id = body[0]
    length = 0
    subpacket = ''
    if length_type_id == '0':
        length = int(body[1:16], 2)
        subpacket = body[16:16+length]
    else:
        length = int(body[1:12], 2)
        subpacket = body[12:]
    return (length_type_id, length, subpacket)


LITERAL_VALUE_TYPE = 4


def parse_packet(packet):
    header, body = split_packet(packet)
    version, type_id = parse_header(header)

    if type_id == LITERAL_VALUE_TYPE:
        value, bits_parsed = get_literal_value(body)
        packet_size = bits_parsed + len(header)

        return (version, packet_size)
    else:
        length_type, num, subpacket = parse_body(body)
        if length_type == '0':
            while len(subpacket):
                s_version, s_bits_parsed = parse_packet(subpacket)
                version += s_version
                subpacket = subpacket[s_bits_parsed:]
                packet_size = num + 15 + len(header) + 1
            return (version, packet_size)
        else:
            packet_size = 11 + len(header) + 1
            for i in range(num):
                s_version, s_bits_parsed = parse_packet(subpacket)
                version += s_version
                subpacket = subpacket[s_bits_parsed:]
                packet_size += s_bits_parsed
            return (version, packet_size)


version_sum = 0
parsed = False
while not parsed:
    version, bits_parsed = parse_packet(packet)
    version_sum += version
    packet = packet[bits_parsed:]

    if '1' not in packet:
        parsed = True


print(version_sum)
