import re
from collections import deque

from helpers import print_peak_memory_used, read_puzzle, timed


@timed
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


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(high_score(puzzle))
    print(high_score(puzzle.replace(' points', '00 points')))
    print_peak_memory_used()
