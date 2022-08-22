from copy import deepcopy
import math
from typing import List, Tuple, Union, Literal


SnailfishNumberPrimitive = Union[Literal['[', ']', ','], int]
SnailfishNumber = List[SnailfishNumberPrimitive]

nums: SnailfishNumber = []
with open('18/input_test.txt') as f:
    nums_raw = f.read().strip().split('\n')
    for nr in nums_raw:
        split_list = []
        skip_next = False
        for i, char in enumerate(nr):
            if skip_next:
                skip_next = False
                continue
            if char.isnumeric():
                next_char = nr[i+1]
                if next_char.isnumeric():
                    split_list.append(int(f'{char}{next_char}'))
                    skip_next = True
                else:
                    split_list.append(int(char))
            else:
                split_list.append(char)
        nums.append(split_list)


def format(num: SnailfishNumber) -> str:
    return "".join([str(c) for c in num])


def add(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    a.append(',')
    merged = a + b
    merged.insert(0, '[')
    merged.append(']')
    return merged


def explode(num_and_index: Tuple[SnailfishNumber, int], new_num_and_index: Tuple[SnailfishNumber, int]):
    num, curr_index = num_and_index
    new_num, recent_int_index = new_num_and_index

    next_int = None
    next_int_index = None
    for i, char in enumerate(num[curr_index + 3:]):
        if isinstance(char, int):
            next_int = char
            next_int_index = curr_index + 3 + i
            break

    if recent_int_index != None:
        left_int = num[curr_index]
        recent_int = new_num[recent_int_index]
        new_num[recent_int_index] = left_int + recent_int

    if next_int_index != None:
        right_int = num[curr_index + 2]
        num[next_int_index] = right_int + next_int

    new_num[-1] = 0


def split(char: int, new_num: SnailfishNumber):
    new_left = math.floor(char / 2)
    new_right = math.ceil(char / 2)
    new_num += ['[', new_left, ',', new_right, ']']


def reduce(num: SnailfishNumber) -> SnailfishNumber:
    OPEN = '['
    CLOSE = ']'

    depth: int = 0
    recent_int_index: Union[int, None] = None
    new_num: SnailfishNumber = []
    split_state = None

    for i, char in enumerate(num):
        if isinstance(char, int):
            # Explode
            if depth > 4:
                explode((num, i), (new_num, recent_int_index))
                reduced_num = new_num + num[i+4:]
                print(f'Exploded: {format(reduced_num)}')
                return reduced_num
            # Splitting is second in priority to explode.
            # If we encounter a int larger than 9, we save the state to run
            # after checking for explodes
            # so we don't have to run through the loop again
            if char >= 10:
                if not split_state:
                    split_state = {'char': char,
                                   'new_num': deepcopy(new_num), 'index': i}

            recent_int_index = len(new_num)
        elif char == OPEN:
            depth += 1
        elif char == CLOSE:
            depth -= 1
        new_num.append(char)

    # Split if we found a splitable condition when checking for explodes
    if split_state:
        split(split_state['char'], split_state['new_num'])
        reduced_num = split_state['new_num'] + num[split_state['index']+1:]
        print(f'Split: {format(reduced_num)}')
        return reduced_num

    return []


res: SnailfishNumber = []
prev_nums: List[SnailfishNumber] = []
for n in nums:
    if prev_nums:
        res = add(prev_nums.pop(), n)

        while True:
            reduced = reduce(res)

            if not reduced:
                break

            res = reduced

        prev_nums.append(res)
    else:
        prev_nums.append(n)

# TEST ALGO
# res = nums[0]
# print(f'Reducing: {format(nums[0])}')
# while True:

#     reduced = reduce(res)

#     if not reduced:
#         break

#     res = reduced
