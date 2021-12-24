state = {}
with open('23/input.txt') as f:
    lines = f.read().strip().splitlines()
    for i, l in enumerate(lines):
        if i == 2:
            state['A1'] = l[3]
            state['B1'] = l[5]
            state['C1'] = l[7]
            state['D1'] = l[9]
        if i == 3:
            state['A2'] = l[3]
            state['B2'] = l[5]
            state['C2'] = l[7]
            state['D2'] = l[9]
    for i in range(1, 12):
        if i > 1:
            state[f'H{i - 1}'] = ''
        if i < 11:
            state[f'H{i + 1}'] = ''


def create_graph():
    graph = {}
    for i in range(1, 12):
        neighbors = []
        if i > 1:
            neighbors.append(f'H{i - 1}')
        if i < 11:
            neighbors.append(f'H{i + 1}')
        if i == 3:
            neighbors.append('A1')
        if i == 5:
            neighbors.append('B1')
        if i == 7:
            neighbors.append('C1')
        if i == 9:
            neighbors.append('D1')
        graph[f'H{i}'] = neighbors

        graph['A1'] = ['H3', 'A2']
        graph['B1'] = ['H5', 'B2']
        graph['C1'] = ['H7', 'C2']
        graph['D1'] = ['H9', 'D2']
        graph['A2'] = ['A1']
        graph['B2'] = ['B1']
        graph['C2'] = ['C1']
        graph['D2'] = ['D1']

    return graph


graph = create_graph()

print(graph)
