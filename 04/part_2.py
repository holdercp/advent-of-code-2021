game_data = []
called_nums = []
boards = []
with open("04/input.txt") as f:
    game_data = f.read().split('\n\n')
    called_nums = game_data[0].split(",")
    boards_raw = [b.splitlines() for b in game_data[1:]]
    boards = []
    for i, b in enumerate(boards_raw):
        boards.append([])
        for r in b:
            boards[i].append(r.split())

mark = 'x'
board_size = len(boards[0][0])
winning_mark = None
winning_boards = []

for called_num in called_nums:
    if len(winning_boards) == 1 and len(boards) == 0:
        break
    else:
        winning_boards = []

    for board in boards:
        c_matches = [0] * board_size
        for r_idx, row in enumerate(board):
            r_matches = 0
            for n_idx, num in enumerate(row):
                if num == called_num:
                    board[r_idx][n_idx] = mark
                if row[n_idx] == mark:
                    c_matches[n_idx] += 1
                    r_matches += 1
            if r_matches == board_size:
                winning_boards.append(board)
                winning_mark = called_num
                break
        if r_matches == board_size:
            continue
        else:
            try:
                if c_matches.index(board_size) > -1:
                    winning_boards.append(board)
                    winning_mark = called_num
            except ValueError:
                continue

    if len(winning_boards) > 0:
        for wb in winning_boards:
            for i, b in enumerate(boards):
                if b == wb:
                    boards.pop(i)
                    break


sum = 0
for row in winning_boards[0]:
    for num in row:
        if num != mark:
            sum += int(num)

print(sum * int(winning_mark))
