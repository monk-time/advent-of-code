import re
from collections import deque

from helpers import read_puzzle


def high_score(s: str) -> int:
    players, last_marble = map(int, re.findall(r'\d+', s))
    scores = [0] * players
    circle = deque([0])
    for marble in range(1, last_marble + 1):
        if marble % 23 != 0:
            circle.rotate(-1)
            circle.append(marble)
        else:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
    return max(scores)


def solve():
    puzzle = read_puzzle()
    return high_score(puzzle), high_score(puzzle.replace(' points', '00 points'))


if __name__ == '__main__':
    print(solve())
