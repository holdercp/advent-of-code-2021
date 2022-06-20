
import json
import copy
from itertools import product
from typing import Dict, Literal, Tuple, TypedDict

player_pos = []
with open('21/input.txt') as f:
    player_data = f.read().strip().splitlines()
    for p in player_data:
        *_, pos = p.split(': ')
        player_pos.append(int(pos))

Player = TypedDict(
    'Player', {'score': int, 'pos': int})
PlayerId = Literal['p1', 'p2']
Universe = TypedDict(
    'Universe', {'p1': Player, 'p2': Player})
Universes = Dict[str, int]


def switch_players(current_player: PlayerId) -> PlayerId:
    return 'p1' if current_player == 'p2' else 'p2'


def move(universe: Universe, roll: int, current_player: PlayerId) -> Universe:
    next_universe = copy.deepcopy(universe)
    moves = ((universe[current_player]['pos'] + roll) % 10) or 10

    next_universe[current_player]['score'] += moves
    next_universe[current_player]['pos'] = moves
    return next_universe


def take_turn(universes: Dict, current_player: PlayerId) -> Tuple[Universes, int]:
    wins = 0
    new_universes = {}

    for universe_serialized, universe_occurences in universes.items():
        universe = json.loads(universe_serialized)
        for roll, roll_freqs in roll_freq_map.items():
            next_universe = move(universe, roll, current_player)
            universe_count = universe_occurences * roll_freqs

            if next_universe[current_player]['score'] >= winning_score:
                wins += universe_count
            else:
                next_universe_serialized = json.dumps(next_universe)
                if next_universe_serialized in new_universes:
                    new_universes[next_universe_serialized] += universe_count
                else:
                    new_universes[next_universe_serialized] = universe_count

    return (new_universes, wins)


rolls = [sum(p) for p in product([1, 2, 3], repeat=3)]
roll_freq_map = {}
for r in rolls:
    if r in roll_freq_map:
        roll_freq_map[r] += 1
    else:
        roll_freq_map[r] = 1
winning_score = 21
total_wins = {
    'p1': 0,
    'p2': 0
}
starting_universe = {
    'p1': {
        'score': 0,
        'pos': player_pos[0]
    },
    'p2': {
        'score': 0,
        'pos': player_pos[1]
    },
}
universes = {}
universes[json.dumps(starting_universe)] = 1

current_player = 'p1'
while len(universes):
    universes, wins = take_turn(universes, current_player)
    total_wins[current_player] += wins
    current_player = switch_players(current_player)


print(max(total_wins['p1'], total_wins['p2']))
