import re

from helpers import read_puzzle, timed


@timed
def high_score(s: str) -> int:
    players, last_marble = map(int, re.findall(r'\d+', s))
    scores = [0] * players
    marble = [None, 0, None]
    marble[0] = marble[2] = marble
    for value in range(1, last_marble + 1):
        if value % 23 != 0:
            a, b = marble[2], marble[2][2]
            marble = [a, value, b]
            a[2] = b[0] = marble
        else:
            for _ in range(7):
                marble = marble[0]
            scores[value % players] += value + marble[1]
            marble[0][2] = marble[2]
            marble = marble[2]
    return max(scores)


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(high_score(puzzle))
    print(high_score(puzzle.replace(' points', '00 points')))
