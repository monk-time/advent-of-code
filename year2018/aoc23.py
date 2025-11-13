# https://adventofcode.com/2018/day/23

import re
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import product
from math import log2
from operator import attrgetter
from typing import Self, cast

from helpers import read_puzzle

type Coord = tuple[int, int, int]
type Box = tuple[Coord, Coord]


@dataclass(frozen=True)
class Bot:
    pos: Coord
    radius: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        x, y, z, r = re.findall(r'-?\d+', s)
        return cls(pos=(int(x), int(y), int(z)), radius=int(r))


def parse(s: str) -> list[Bot]:
    return [Bot.from_str(line) for line in s.splitlines()]


def dist(a: Coord, b: Coord) -> int:
    return sum(abs(a[i] - b[i]) for i in range(3))


def is_in_range(source: Bot, other: Bot) -> bool:
    return (dist(source.pos, other.pos)) <= source.radius


def count_in_range(bots: list[Bot]) -> int:
    best_bot = max(bots, key=attrgetter('radius'))
    return sum(is_in_range(best_bot, b) for b in bots)


# Part 2 copied from a solution by fizbin:
# https://www.reddit.com/r/adventofcode/comments/a8s17l/_/ecfmpy0/
def does_intersect(box: Box, bot: Bot) -> bool:
    d = 0
    for i in range(3):
        boxlow, boxhigh = box[0][i], box[1][i] - 1
        d += abs(bot.pos[i] - boxlow) + abs(bot.pos[i] - boxhigh)
        d -= boxhigh - boxlow
    d //= 2
    return d <= bot.radius


def intersect_count(box: Box, bots: list[Bot]):
    return sum(1 for b in bots if does_intersect(box, b))


def shortest_manhattan(bots: list[Bot]):
    # Find a box big enough to contain everything in range
    maxabscord = max(
        max(abs(b.pos[i]) + b.radius for b in bots) for i in range(3)
    )
    size: int = 2 ** int(log2(maxabscord))
    initial_box = ((-size, -size, -size), (size, size, size))

    workheap = [(-len(bots), -2 * size, 3 * size, initial_box)]
    while workheap:
        (_negreach, negsz, dist_to_orig, box_) = heappop(workheap)
        if negsz == -1:
            return dist_to_orig
        newsz = negsz // -2
        for octant in product(range(2), repeat=3):
            newbox0 = cast(
                'Coord',
                tuple(box_[0][i] + newsz * octant[i] for i in range(3)),
            )
            newbox1 = cast(
                'Coord',
                tuple(newbox0[i] + newsz for i in range(3)),
            )
            newbox = (newbox0, newbox1)
            newreach = intersect_count(newbox, bots)
            heappush(
                workheap, (-newreach, -newsz, dist(newbox0, (0, 0, 0)), newbox)
            )
    return None


def solve():
    bots = parse(read_puzzle())
    return count_in_range(bots), shortest_manhattan(bots)


if __name__ == '__main__':
    print(solve())
