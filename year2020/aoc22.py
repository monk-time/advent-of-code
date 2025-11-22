# https://adventofcode.com/2020/day/22

from collections import defaultdict, deque
from itertools import count

from utils_proxy import read_puzzle

type Deck = tuple[int, ...]
type Players = tuple[Deck, Deck]
type State = tuple[Deck, Deck, int]


def parse(s: str) -> Players:
    p1, p2 = s.split('\n\n')
    return (
        tuple(int(x) for x in p1.splitlines()[1:]),
        tuple(int(x) for x in p2.splitlines()[1:]),
    )


def combat(p1: Deck, p2: Deck) -> Deck:
    d1, d2 = deque(p1), deque(p2)
    winner = d1  # will be reassigned
    while d1 and d2:
        c1, c2 = d1.popleft(), d2.popleft()
        winner = d1 if c1 > c2 else d2
        winner.extend([max(c1, c2), min(c1, c2)])
    return tuple(winner)


def score(winner: Deck) -> int:
    n = len(winner)
    return sum(x * (n - i) for i, x in enumerate(winner))


def recursive_combat(p1: Deck, p2: Deck) -> Deck:
    counter = count(1)
    seen: dict[int, set[Players]] = defaultdict(set)

    def rec(p1: Deck, p2: Deck, game: int) -> tuple[Deck, Deck, int]:
        while True:
            if not (p1 and p2):
                return p1, p2, int(not p1)
            if (ps := (p1, p2)) in seen[game]:
                return p1, p2, 0
            seen[game].add(ps)
            # Major optimization: p1 can never lose the top card
            top = max(*p1, *p2)
            if game > 1 and top > len(p1) + len(p2) - 2 and top in p1:
                return p1, p2, 0
            c1, c2 = p1[0], p2[0]
            if c1 < len(p1) and c2 < len(p2):
                win = rec(p1[1 : 1 + c1], p2[1 : 1 + c2], next(counter))[2]
            else:
                win = int(c1 < c2)
            extra: list[Deck] = [(), ()]
            extra[win] = (ps[win][0], ps[1 - win][0])
            p1 = (*p1[1:], *extra[0])
            p2 = (*p2[1:], *extra[1])

    p1, p2, win = rec(p1, p2, next(counter))
    return (p1, p2)[win]


def solve() -> tuple[int, int]:
    p1, p2 = parse(read_puzzle())
    return score(combat(p1, p2)), score(recursive_combat(p1, p2))


if __name__ == '__main__':
    print(solve())
