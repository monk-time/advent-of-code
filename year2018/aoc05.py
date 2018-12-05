from string import ascii_lowercase

from helpers import read_puzzle

reacting_pairs = {pair for c in ascii_lowercase for pair in (c + c.upper(), c.upper() + c)}


def are_matching(a: str, b: str) -> bool:
    return a != b and (a.lower() == b or b.lower() == a)
    # return a + b in reacting_pairs


def react(poly: str):
    i = 0
    while i < len(poly) - 1:
        if are_matching(poly[i], poly[i + 1]):
            poly = poly[:i] + poly[i + 2:]
            if i > 0:
                i -= 1
        else:
            i += 1
    return poly


def improve(poly: str) -> int:
    units = set(poly.lower())
    new_polymers = [''.join(c for c in poly if c.lower() != unit) for unit in units]
    return min(len(react(p)) for p in new_polymers)


if __name__ == '__main__':
    poly_ = read_puzzle()
    print(len(react(poly_)), improve(poly_))
