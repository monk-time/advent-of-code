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


if __name__ == '__main__':
    poly_ = react(read_puzzle())
    print(len(poly_), improve(poly_))
