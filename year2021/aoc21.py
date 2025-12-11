# https://adventofcode.com/2021/day/21
# tags: #exponential-growth #recursion

import re
from collections import Counter, deque
from dataclasses import dataclass
from functools import cache
from itertools import product

from utils_proxy import read_puzzle

type Players = tuple[Player, Player]


@dataclass(frozen=True)
class Player:
    pos: int
    score: int = 0

    def advance(self, roll: int) -> Player:
        pos = (self.pos + roll - 1) % 10 + 1
        return Player(pos=pos, score=self.score + pos)


def parse(s: str) -> tuple[Player, Player]:
    _, a, _, b = re.findall(r'\d+', s)
    return Player(int(a)), Player(int(b))


def play_deterministic(players: Players) -> int:
    die = 0
    queue = deque(players)
    while True:
        pl = queue.popleft()
        roll = 3 + die % 100 + (die + 1) % 100 + (die + 2) % 100
        die += 3
        pl_new = pl.advance(roll)
        if pl_new.score >= 1000:
            loser = queue.pop()
            return loser.score * die
        queue.append(pl_new)


def play_dirac(players: Players) -> int:
    @cache
    def count_rec(pl1: Player, pl2: Player) -> tuple[int, int]:
        if pl2.score >= 21:
            return (0, 1)
        wins = [0, 0]
        for roll, count in dice_sums.items():
            pl1_new = pl1.advance(roll)
            win_b, win_a = count_rec(pl2, pl1_new)
            wins[0] += count * win_a
            wins[1] += count * win_b
        return wins[0], wins[1]

    dice_sums = Counter(sum(p) for p in product(range(1, 4), repeat=3))
    return max(count_rec(*players))


def solve() -> tuple[int, int]:
    players = parse(read_puzzle())
    return play_deterministic(players), play_dirac(players)


if __name__ == '__main__':
    print(solve())
