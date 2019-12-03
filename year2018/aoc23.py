import re
from heapq import heappop, heappush
from itertools import product
from math import log2
from typing import List, Tuple

from helpers import read_puzzle

Bot = Tuple[int, ...]


def parse(s: str) -> List[Bot]:
    return [tuple(int(x) for x in re.findall(r'-?\d+', line))
            for line in s.splitlines()]


def dist(a: Bot, b: Bot):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def is_in_range(source: Bot, other: Bot) -> bool:
    return (dist(source, other)) <= source[3]


def count_in_range(bots: List[Bot]) -> int:
    best_bot = max(bots, key=lambda b: b[3])
    return sum(is_in_range(best_bot, b) for b in bots)


# Part 2 copied from a solution by fizbin:
# https://www.reddit.com/r/adventofcode/comments/a8s17l/_/ecfmpy0/
def does_intersect(box, bot: Bot) -> bool:
    d = 0
    for i in range(3):
        boxlow, boxhigh = box[0][i], box[1][i] - 1
        d += abs(bot[i] - boxlow) + abs(bot[i] - boxhigh)
        d -= boxhigh - boxlow
    d //= 2
    return d <= bot[3]


def intersect_count(box, bots):
    return sum(1 for b in bots if does_intersect(box, b))


def shortest_manhattan(bots: List[Bot]):
    # Find a box big enough to contain everything in range
    maxabscord = max(max(abs(b[i]) + b[3] for b in bots) for i in range(3))
    size = 2 ** int(log2(maxabscord))
    initial_box = ((-size, -size, -size), (size, size, size))

    workheap = [(-len(bots), -2 * size, 3 * size, initial_box)]
    while workheap:
        (negreach, negsz, dist_to_orig, box_) = heappop(workheap)
        if negsz == -1:
            return dist_to_orig
        newsz = negsz // -2
        for octant in product(range(2), repeat=3):
            newbox0 = tuple(box_[0][i] + newsz * octant[i] for i in range(3))
            newbox1 = tuple(newbox0[i] + newsz for i in range(3))
            newbox = (newbox0, newbox1)
            newreach = intersect_count(newbox, bots)
            heappush(workheap,
                     (-newreach, -newsz, dist(newbox0, (0, 0, 0)), newbox))


def solve():
    bots = parse(read_puzzle())
    return count_in_range(bots), shortest_manhattan(bots)


if __name__ == '__main__':
    print(solve())
