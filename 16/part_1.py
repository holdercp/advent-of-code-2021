packet_bin = ''
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
    subpackets = 0
    if length_type_id == '0':
        length = int(body[1:16], 2)
        subpackets = body[16:]
    else:
        length = int(body[1:12], 2)
        subpackets = body[12:]
    return (length_type_id, length, subpackets)


def get_padding(packet_size):
    remainder = packet_size % 4
    return 4 - remainder


literal_value_type = 4


def parse_packets(packets):
    header, body = split_packet(packets)
    version, type_id = parse_header(header)

    if type_id == literal_value_type:
        value, bits_parsed = get_literal_value(body)
        packet_size = bits_parsed + len(header)
        padding = get_padding(packet_size)

        return (version, value, packet_size + padding)
    else:
        length_type, num, subpackets = parse_body(body)
        if length_type == '0':
            bits_parsed = 0
            while bits_parsed < num:
                s_version, s_value, s_bits_parsed = parse_packets(subpackets)
                version += s_version
                bits_parsed += s_bits_parsed
                subpackets = subpackets[bits_parsed:]
            return (version, 0, bits_parsed)
        else:
            bits_parsed = 0
            for i in range(num):
                s_version, s_value, s_bits_parsed = parse_packets(subpackets)
                bits_parsed += s_bits_parsed
                subpackets = subpackets[s_bits_parsed:]
                version += s_version
            return (version, 0, bits_parsed)


version_sum = 0
while len(packet) > 0:
    version, value, bits_parsed = parse_packets(packet)
    version_sum += version
    packet = packet[bits_parsed:]


print(version_sum)
