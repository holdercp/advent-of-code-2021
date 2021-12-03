report = []
with open("03/input.txt") as f:
    report = f.read().splitlines()

gammaRate = ''
epsilonRate = ''
bitSize = len(report[0])
for bit in range(bitSize):
    total = 0
    for num in report:
        total += int(num[bit])

    if total >= len(report) / 2:
        gammaRate += "1"
        epsilonRate += "0"
    else:
        gammaRate += "0"
        epsilonRate += "1"

print(int(gammaRate, 2) * int(epsilonRate, 2))
