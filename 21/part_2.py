from collections import deque
import copy
from itertools import product

player_pos = []
with open('21/input.txt') as f:
    player_data = f.read().strip().splitlines()
    for p in player_data:
        *_, pos = p.split(': ')
        player_pos.append(int(pos))

winning_score = 21
rolls = [3, 4, 5, 4, 5, 5, 6, 6, 7, 4, 5, 6, 5,
         6, 6, 7, 7, 8, 5, 6, 7, 6, 7, 7, 8, 8, 9]
wins = {
    'p1': 0,
    'p2': 0
}
p1 = {
    'id': 'p1',
    'score': 0,
    'pos': player_pos[0]
}
p2 = {
    'id': 'p2',
    'score': 0,
    'pos': player_pos[1]
}
starting_state = {
    'p1': p1,
    'p2': p2,
    'current_player': p1,
    'u_count': 1,
}
d = deque()
d.append(starting_state)

while len(d) > 0:
    universe = d.pop()
    for r in rolls:
        cp = universe['current_player']
        moves = cp['pos'] + r % 10 or 10

        if cp['score'] + moves >= winning_score:
            wins[cp['id']] += universe['u_count'] + 27
        else:
            next_u = copy.deepcopy(universe)
            next_u[cp['id']]['score'] += moves
            next_u[cp['id']]['pos'] = moves
            next_u['u_count'] += 27
            next_u['current_player'] = next_u['p1'] if next_u['current_player'] == next_u['p2'] else next_u['p2']
            d.append(next_u)
print(wins)
