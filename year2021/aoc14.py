# https://adventofcode.com/2021/day/14
# tags: #frequency #instructions #exponential-growth

import re
from collections import Counter
from itertools import pairwise, starmap

from helpers import read_puzzle

type Pair = tuple[str, str]
type Rules = dict[Pair, str]
type Pairs = Counter[Pair]
type Poly = Counter[str]


def parse(s: str) -> tuple[Pairs, Rules]:
    poly, s2 = s.split('\n\n')
    rules = {
        (t[0], t[1]): t[2]
        for line in s2.splitlines()
        if (t := re.findall(r'[A-Z]', line))
    }
    return Counter(pairwise(f'_{poly}_')), rules


def next_step(pairs: Pairs, rules: Rules) -> Pairs:
    def expand(p: Pair, n: int) -> Pairs:
        x, y = p
        inner = {(x, rules[p]): n, (rules[p], y): n} if p in rules else {p: n}
        return Counter(inner)

    return sum(starmap(expand, pairs.items()), Counter[Pair]())


def merge(pairs: Pairs) -> Poly:
    poly = Counter[str]()
    for (a, b), count in pairs.items():
        poly[a] += count
        poly[b] += count
    del poly['_']
    return Counter({x: count // 2 for x, count in poly.items()})


def score(pairs: Pairs, rules: Rules, steps: int) -> int:
    for _ in range(steps):
        pairs = next_step(pairs, rules)
    counts = merge(pairs).most_common()
    return counts[0][1] - counts[-1][1]


def solve() -> tuple[int, int]:
    poly, rules = parse(read_puzzle())
    return score(poly, rules, 10), score(poly, rules, 40)


if __name__ == '__main__':
    print(solve())
