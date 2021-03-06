import re
from collections import Counter, namedtuple
from itertools import product
from typing import Iterable, List, Tuple

from helpers import read_puzzle

Claim = namedtuple('Claim', 'id left top width height')


def parse(claim: str) -> Claim:
    return Claim(*map(int, re.findall(r'\d+', claim)))


def parse_puzzle() -> List[Claim]:
    return [parse(line) for line in read_puzzle().splitlines()]


def squares(a: Claim) -> Iterable[Tuple[int, int]]:
    return product(range(a.left, a.left + a.width), range(a.top, a.top + a.height))


def overlap_and_count(claims: List[Claim]):
    layers = Counter(sq for c in claims for sq in squares(c))
    inches = sum(1 for v in layers.values() if v > 1)
    unused_id = next(c.id for c in claims if all(layers[sq] == 1 for sq in squares(c)))
    return inches, unused_id


def solve():
    return overlap_and_count(parse_puzzle())


if __name__ == '__main__':
    print(solve())
