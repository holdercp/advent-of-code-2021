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
row_length = len(boards[0][0])
winning_board = None
winning_mark = None

for called_num in called_nums:
    for board in boards:
        c_matches = [0] * row_length
        for r_idx, row in enumerate(board):
            r_matches = 0
            for n_idx, num in enumerate(row):
                if num == called_num:
                    board[r_idx][n_idx] = mark
                if row[n_idx] == mark:
                    c_matches[n_idx] += 1
                    r_matches += 1
            if r_matches == row_length:
                winning_board = board
                winning_mark = called_num
                break
        if winning_board:
            break
        try:
            if c_matches.index(row_length):
                winning_board = board
                winning_mark = called_num
                break
        except ValueError:
            continue
    if winning_board:
        break

sum = 0
for row in winning_board:
    for num in row:
        if num != mark:
            sum += int(num)

print(sum * int(winning_mark))
