from typing import Iterable

from helpers import read_puzzle


def are_matching(a: str, b: str) -> bool:
    return a != b and (a.lower() == b or b.lower() == a)


def react(poly: Iterable[str], skip: str = None) -> str:
    new_poly = ''
    for unit in iter(poly):
        if unit.lower() == skip:
            continue
        if new_poly and are_matching(unit, new_poly[-1]):
            new_poly = new_poly[:-1]
        else:
            new_poly += unit
    return new_poly


def improve(poly: str) -> int:
    units = set(poly.lower())
    return min(len(react(poly, skip=unit)) for unit in units)


def solve():
    poly = react(read_puzzle())
    return len(poly), improve(poly)


if __name__ == '__main__':
    print(solve())
