initial_state = {}
with open('23/input.txt') as f:
    lines = f.read().strip().splitlines()
    for i, l in enumerate(lines):
        if i == 2:
            initial_state['A1'] = l[3]
            initial_state['B1'] = l[5]
            initial_state['C1'] = l[7]
            initial_state['D1'] = l[9]
        if i == 3:
            initial_state['A2'] = l[3]
            initial_state['B2'] = l[5]
            initial_state['C2'] = l[7]
            initial_state['D2'] = l[9]


def add_room_graph(graph, state):
    for loc in state.keys():
        room_type, room_num = loc
        graph[loc] = {}

        neighbors = []
        if room_num == '1':
            if room_type == 'A':
                neighbors.append('H3')
            if room_type == 'B':
                neighbors.append('H5')
            if room_type == 'C':
                neighbors.append('H7')
            if room_type == 'D':
                neighbors.append('H9')

        if int(room_num) > 1:
            neighbors.append(f'{room_type}{int(room_num) - 1}')
        if int(room_num) < 2:
            neighbors.append(f'{room_type}{int(room_num) + 1}')

        graph[loc] = neighbors

    return graph


def add_hallway_graph(graph):
    for i in range(1, 12):
        loc = f'H{i}'
        graph[loc] = {}

        neighbors = []
        room_type = loc[0]
        room_num = loc[1:]
        if i > 1:
            neighbors.append(f'{room_type}{int(room_num) - 1}')
        if i < 11:
            neighbors.append(f'{room_type}{int(room_num) + 1}')

        if i == 3:
            neighbors.append('A1')
        if i == 5:
            neighbors.append('B1')
        if i == 7:
            neighbors.append('C1')
        if i == 9:
            neighbors.append('D1')
        graph[loc] = neighbors

    return graph


def create_graph(state):
    graph = {}
    graph = add_room_graph(graph, state)
    graph = add_hallway_graph(graph)
    return graph


cost_multipliers = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


def is_room(loc):
    return loc[0] != 'H'


def should_move(pod, loc, state):
    # If pod is in incorrect room
    if pod != loc[0]:
        return True

    # Or if pod is blocking an incorrect pod
    if loc[1] == '1':
        if f'{loc[0]}2' in state and state[f'{loc[0]}2'] != pod:
            return True

    # Or pod is in hallway
    if not is_room(loc):
        return True

    # Else don't move
    return False


def find_hallway_moves(loc, state, graph, energy_count=0, visited=[]):
    visited.append(loc)
    neighbors = [n for n in graph[loc] if n not in visited and n not in state]

    if len(neighbors) == 0:
        return []

    hallway_moves = []
    for n in neighbors:
        if n[0] == 'H' and n[1] not in ['3', '5', '7', '9']:
            hallway_moves.append((energy_count + 1, n))
        hallway_moves += \
            find_hallway_moves(n, state, graph, energy_count + 1, visited)
    return hallway_moves


def find_room_moves(pod, loc, state, graph, energy_count=0, visited=[]):
    visited.append(loc)
    neighbors = [n for n in graph[loc]
                 if n not in visited and n not in state and (n[0] == pod or n[0] == 'H')]

    if len(neighbors) == 0:
        return []

    room_moves = []
    for n in neighbors:
        if n[0] == pod:
            if n[1] == '2':
                room_moves.append((energy_count + 1, n))
            if n[1] == '1' and (f'{n[0]}2' in state and state[f'{n[0]}2'] == pod):
                room_moves.append((energy_count + 1, n))
        room_moves += \
            find_room_moves(pod, n, state, graph, energy_count + 1, visited)
    return room_moves


def get_valid_moves(pod, loc, state, graph):
    if is_room(loc):
        return find_hallway_moves(loc, state, graph, 0, [])
    else:
        return find_room_moves(pod, loc, state, graph, 0, [])


def update_state(pod, current, destination, state):
    updated_state = state.copy()

    del updated_state[current]
    updated_state[destination] = pod

    return updated_state


def org_pods(graph, initial_state):
    target = (('A1', 'A'), ('A2', 'A'), ('B1', 'B'),
              ('B2', 'B'), ('C1', 'C'), ('C2', 'C'), ('D1', 'D'), ('D2', 'D'))
    q = [(0, initial_state)]
    states = {}
    states[tuple(sorted(initial_state.items()))] = 0

    while len(q) > 0:
        q.sort(key=lambda s: s[0])
        energy, state_tuple = q.pop()
        state = dict(state_tuple)

        for loc, pod in state.items():
            if should_move(pod, loc, state):
                valid_moves = get_valid_moves(pod, loc, state, graph)
                for m in valid_moves:
                    energy_cost, new_loc = m
                    total_energy = energy + \
                        (energy_cost * cost_multipliers[pod])
                    new_state = update_state(pod, loc, new_loc, state)
                    key = tuple(sorted(new_state.items()))

                    if key not in states or total_energy < states[key]:
                        q.append((total_energy, key))
                        states[key] = total_energy
    organized_pods = [e for s, e in states.items() if s == target]
    return min(organized_pods)


graph = create_graph(initial_state)
result = org_pods(graph, initial_state)

print(result)
