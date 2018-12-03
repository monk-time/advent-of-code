import re
from collections import namedtuple
from itertools import chain, combinations, product
from typing import Iterable, List, Optional, Tuple

from helpers import read_puzzle

Claim = namedtuple('Claim', 'id left top width height')


def parse(claim: str) -> Claim:
    return Claim(*[int(n) for n in re.findall(r'\d+', claim)])


def overlap(a: Claim, b: Claim) -> Optional[Claim]:
    left, right = max(a.left, b.left), min(a.left + a.width, b.left + b.width)
    top, bottom = max(a.top, b.top), min(a.top + a.height, b.top + b.height)
    if left >= right or top >= bottom:
        return None
    return Claim((a.id, b.id), left, top, right - left, bottom - top)


def claim_to_points(a: Claim) -> Iterable[Tuple[int, int]]:
    return product(range(a.left, a.left + a.width), range(a.top, a.top + a.height))


def overlap_all(claims: List[Claim]) -> Iterable[Claim]:
    for a, b in combinations(claims, 2):
        o = overlap(a, b)
        if o:
            yield o


def solve(claims: List[Claim]):
    overlaps = list(overlap_all(claims))
    points = map(claim_to_points, overlaps)
    inches = len(set(chain.from_iterable(points)))
    ids = [c.id for c in claims]
    used_ids = set(chain.from_iterable(c.id for c in overlaps))
    unused = next(id_ for id_ in ids if id_ not in used_ids)
    return inches, unused


if __name__ == '__main__':
    puzzle = [parse(line) for line in read_puzzle().splitlines()]
    print(solve(puzzle))
