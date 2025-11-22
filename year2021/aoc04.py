# https://adventofcode.com/2021/day/4
# tags: #grid #multidimensional-grid

import re
from collections import defaultdict
from typing import NewType

from utils_proxy import read_puzzle

Num = NewType('Num', int)  # a number on a bingo board
BoardIdx = NewType('BoardIdx', int)
type Coord = tuple[int, int]
type Coord3 = tuple[Coord, BoardIdx]
type Board = dict[Coord, Num]

SIZE = 5


def parse(s: str) -> tuple[list[Num], list[Board]]:
    s_nums, *s_boards = s.split('\n\n')
    nums = [Num(int(n)) for n in s_nums.split(',')]
    boards = [
        {
            divmod(i, SIZE): Num(int(x))
            for i, x in enumerate(re.findall(r'\d+', board))
        }
        for board in s_boards
    ]
    return nums, boards


def play_bingo(nums: list[Num], boards: list[Board]) -> tuple[int, int]:
    num_locations = defaultdict[Num, set[Coord3]](set)
    for b, board in enumerate(boards):
        for pos, num in board.items():
            num_locations[num].add((pos, BoardIdx(b)))
    marked = set[Coord3]()
    line_counters: list[list[int]] = [[0] * (SIZE * 2) for _ in boards]
    won_boards = set[BoardIdx]()
    scores: list[int] = []
    for num in nums:
        for (i, j), b in num_locations[num]:
            if b in won_boards:
                continue
            marked.add(((i, j), b))
            counter = line_counters[b]
            counter[i] += 1
            counter[j + SIZE] += 1
            if counter[i] < SIZE and counter[j + SIZE] < SIZE:
                continue
            won_boards.add(b)
            if 1 < len(won_boards) < len(boards):
                continue
            board = boards[b]
            unmarked = (board[pos] for pos in board if (pos, b) not in marked)
            scores.append(sum(unmarked) * num)
    return scores[0], scores[1]


def solve() -> tuple[int, int]:
    nums, boards = parse(read_puzzle())
    return play_bingo(nums, boards)


if __name__ == '__main__':
    print(solve())
