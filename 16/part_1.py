with open('16/input.txt') as f:
    transmission = f.read().strip()
    # https://stackoverflow.com/a/58290165
    bin_str = bin(int(transmission, 16))[2:]
    padding = (4-len(bin_str) % 4) % 4
    packet = '0'*padding+bin_str


def split_packet(packet):
    header = packet[:6]
    body = packet[6:]
    return (header, body)


def parse_header(header):
    version = header[:3]
    type_id = header[3:]

    return (int(version, 2), int(type_id, 2))


def get_literal_value(literal_value):
    bin_str = ''
    step = 5
    bits_parsed = 0
    for i in range(0, len(literal_value), step):
        bin_str += literal_value[i+1:i+step]
        if literal_value[i] == '0':
            bits_parsed = i+step
            break
    return (int(bin_str, 2), bits_parsed)


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


literal_value_type = 4


def parse_packet(packet):
    header, body = split_packet(packet)
    version, type_id = parse_header(header)

    if type_id == literal_value_type:
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
