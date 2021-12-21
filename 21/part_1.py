player_pos = []
with open('21/input.txt') as f:
    player_data = f.read().strip().splitlines()
    for p in player_data:
        *_, pos = p.split(': ')
        player_pos.append(int(pos))


def roll_deterministic(die):
    moves = die['roll'] + (die['roll'] + 1) + (die['roll'] + 2)
    die['roll'] = 100 if (
        die['roll'] + 3) % 100 == 0 else (die['roll'] + 3) % 100
    die['count'] += 3
    return moves


def take_turn(player, die):
    moves = roll_deterministic(die)
    space = 10 if (player['pos'] +
                   moves) % 10 == 0 else (player['pos'] + moves) % 10
    player['pos'] = space
    player['score'] += space


p1 = {
    'score': 0,
    'pos': player_pos[0]
}
p2 = {
    'score': 0,
    'pos': player_pos[1]
}

die = {
    'roll': 1,
    'count': 0
}
current_player = p1
while p1['score'] < 1000 > p2['score']:
    take_turn(current_player, die)
    current_player = p1 if current_player == p2 else p2

print(die['count'] * current_player['score'])
