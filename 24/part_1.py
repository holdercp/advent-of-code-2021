monad_chunks = [[] for _ in range(14)]
with open('24/input.txt') as f:
    commands = f.read().strip().splitlines()
    input_count = -1
    for c in commands:
        op, opd_1, *opd_2 = c.split()
        if op == 'inp':
            input_count += 1
        opd_2 = opd_2[0] if len(opd_2) == 1 else None
        monad_chunks[input_count].append((op, opd_1, opd_2))


def ALU(input, program, initial_state):
    x, y, z = initial_state
    mem = {'x': x, 'y': y, 'z': z, 'w': 0}

    for instruction in program:
        op, opd_1, opd_2 = instruction

        if op == 'add':
            mem[opd_1] += int(opd_2) if opd_2.isdigit() or opd_2[0] == '-' else mem[opd_2]
        elif op == 'mul':
            mem[opd_1] *= int(opd_2) if opd_2.isdigit() or opd_2[0] == '-' else mem[opd_2]
        elif op == 'div':
            mem[opd_1] = int(
                mem[opd_1] / int(opd_2)) if opd_2.isdigit() or opd_2[0] == '-' else int(mem[opd_1] / mem[opd_2])
        elif op == 'mod':
            mem[opd_1] %= int(opd_2) if opd_2.isdigit(
            ) or opd_2[0] == '-' else mem[opd_2]
        elif op == 'eql':
            opd = int(opd_2) if opd_2.isdigit(
            ) or opd_2[0] == '-' else mem[opd_2]
            mem[opd_1] = 1 if mem[opd_1] == opd else 0
        elif op == 'inp':
            mem[opd_1] = input

    return (mem['x'], mem['y'], mem['z'])


states = {(0, 0, 0): ''}
for chunk in monad_chunks:
    new_states = {}
    for state, prev_digits in states.items():
        for digit in reversed(range(1, 10)):
            result = ALU(digit, chunk, state)
            if result not in new_states.keys():
                new_states[result] = prev_digits + str(digit)
    states = new_states
print([s for k, s in states.items() if k[2] == 0])
