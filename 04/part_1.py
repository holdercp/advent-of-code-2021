game_data = []
drawn_nums = []
boards = []
with open("04/input.txt") as f:
    game_data = f.read().split('\n\n')
    drawn_nums = game_data[0]
    boards_raw = [b.splitlines() for b in game_data[1:]]
    boards = []
    for i, b in enumerate(boards_raw):
        boards.append([])
        for r in b:
            boards[i].append(r.split())
