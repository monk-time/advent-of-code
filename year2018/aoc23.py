import re
from dataclasses import dataclass
from typing import List, Tuple

from helpers import read_puzzle

Point = Tuple[int, int, int]


@dataclass
class Nanobot:
    pos: Point
    r: int

    def is_in_range(self, other) -> bool:
        return (abs(self.pos[0] - other.pos[0]) +
                abs(self.pos[1] - other.pos[1]) +
                abs(self.pos[2] - other.pos[2])) <= self.r


def parse(s: str) -> List[Nanobot]:
    return [Nanobot(m[:3], m[3])
            for line in s.splitlines()
            if (m := tuple(int(x) for x in re.findall(r'-?\d+', line)))]


def count_in_range(bots: List[Nanobot]) -> int:
    best_bot = max(bots, key=lambda b: b.r)
    return sum(best_bot.is_in_range(b) for b in bots)


def shortest_manhattan(bots: List[Nanobot]):
    pass


def solve():
    bots = parse(read_puzzle())
    return count_in_range(bots)


if __name__ == '__main__':
    print(solve())
