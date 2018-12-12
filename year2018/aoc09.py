import re
from dataclasses import dataclass, field

from helpers import read_puzzle, timed


@dataclass
class Marble:
    value: int
    prev: 'Marble' = field(default=None, repr=False)
    next: 'Marble' = field(default=None, repr=False)


@timed
def high_score(s: str) -> int:
    players, last_marble = map(int, re.findall(r'\d+', s))
    marble, scores = Marble(0), [0] * players
    marble.prev, marble.next = marble, marble
    for value in range(1, last_marble + 1):
        if value % 23 != 0:
            a, b = marble.next, marble.next.next
            marble = Marble(value, prev=a, next=b)
            a.next = b.prev = marble
        else:
            for _ in range(7):
                marble = marble.prev
            scores[value % players] += value + marble.value
            marble.prev.next = marble.next
            marble = marble.next
    return max(scores)


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(high_score(puzzle))
    print(high_score(puzzle.replace(' points', '00 points')))
