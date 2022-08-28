from enum import Enum


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


def parse_operation(body, calc_func, result):
    length_type, num, subpacket = parse_body(body)
    packet_size = 7 + (num + 15 if length_type == '0' else 11)

    while subpacket if length_type == '0' else num:
        value, bits_parsed = parse_packet(subpacket)
        subpacket = subpacket[bits_parsed:]

        result = calc_func(value, result)

        if length_type == '1':
            packet_size += bits_parsed
            num -= 1

    return (result, packet_size)


def parse_literal(literal_value):
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

    return (int(value, 2), bits_parsed + 6)


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


class PacketTypes(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


def parse_packet(packet):
    header, body = split_packet(packet)
    version, type_id = parse_header(header)

    if type_id == PacketTypes.SUM.value:
        def add(v, r):
            return r + v

        return parse_operation(body, add, 0)

    if type_id == PacketTypes.PRODUCT.value:
        def muliply(v, r):
            return r * v

        return parse_operation(body, muliply, 1)

    if type_id == PacketTypes.MINIMUM.value:
        return parse_operation(body, min, 1000000000)

    if type_id == PacketTypes.MAXIMUM.value:
        return parse_operation(body, max, -1000000000)

    if type_id == PacketTypes.LITERAL.value:
        return parse_literal(body)

    if type_id == PacketTypes.GREATER_THAN.value:
        def greater_than(second, first):
            if first == None:
                return second

            return 1 if first > second else 0

        return parse_operation(body, greater_than, None)

    if type_id == PacketTypes.LESS_THAN.value:
        def less_than(second, first):
            if first == None:
                return second

            return 1 if first < second else 0

        return parse_operation(body, less_than, None)

    if type_id == PacketTypes.EQUAL_TO.value:
        def equal_to(second, first):
            if first == None:
                return second

            return 1 if first == second else 0

        return parse_operation(body, equal_to, None)

    raise Exception(f'invalid type: {type_id}')


value, bits_parsed = parse_packet(packet)
print(value)
