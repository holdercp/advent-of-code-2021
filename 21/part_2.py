from collections import deque
import copy
from itertools import product
from typing import Literal, TypedDict

player_pos = []
with open('21/input.txt') as f:
    player_data = f.read().strip().splitlines()
    for p in player_data:
        *_, pos = p.split(': ')
        player_pos.append(int(pos))

player = TypedDict(
    'Player', {'id': Literal['p1', 'p2'], 'score': int, 'pos': int})
universe = TypedDict(
    'Universe', {'p1': player, 'p2': player, 'current_player': player})


def serializeUniverse(universe: universe, roll: int) -> str:
    p1, p2, current_player = universe.values()
    return f'{p1["id"]}:({p1["score"]},{p1["pos"]}),{p2["id"]}:({p2["score"]},{p2["pos"]}),cp:{current_player["id"]},m:{roll}'


winning_score = 21
rolls = [sum(p) for p in product([1, 2, 3], repeat=3)]
rollsDict = {}
for r in rolls:
    if r in rollsDict:
        rollsDict[r] += 1
    else:
        rollsDict[r] = 1
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
}
universes = deque()
universes.append(starting_state)

seenUniverses = set()

while len(universes) > 0:
    universe = universes.pop()
    for roll, occurences in rollsDict.items():
        cp = universe['current_player']
        moves = ((cp['pos'] + roll) % 10) or 10
        universeState = serializeUniverse(universe=universe, roll=roll)

        if universeState in seenUniverses:
            wins[cp['id']] += occurences
        elif cp['score'] + moves >= winning_score:
            wins[cp['id']] += occurences
            seenUniverses.add(universeState)
        else:
            next_u = copy.deepcopy(universe)
            next_u[cp['id']]['score'] += moves
            next_u[cp['id']]['pos'] = moves
            next_u['current_player'] = next_u['p1'] if next_u['current_player'] == next_u['p2'] else next_u['p2']
            universes.append(next_u)
print(wins)
