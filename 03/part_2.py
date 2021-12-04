report = []
with open('03/input.txt') as f:
    report = f.read().splitlines()


def determine_rating(nums, pos, criteria, criteria_func):
    if len(nums) == 1:
        return nums[0]

    ones = 0
    for num in nums:
        ones += int(num[pos])
    criteria += criteria_func(ones, len(nums))
    subset = [n for n in nums if n.startswith(criteria)]

    return determine_rating(subset, pos+1, criteria, criteria_func)


def ogr_criteria(ones, total):
    return '1' if ones >= total / 2 else '0'


def csr_criteria(ones, total):
    return '1' if ones < total / 2 else '0'


ogr = determine_rating(report.copy(), 0, '', ogr_criteria)
csr = determine_rating(report.copy(), 0, '', csr_criteria)
lsr = int(ogr, 2) * int(csr, 2)

print(lsr)
