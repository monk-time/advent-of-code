# https://adventofcode.com/2021/day/20
# tags: #grid #cellular-automaton

from functools import cache
from itertools import product

from utils_proxy import read_puzzle

type Coord = tuple[int, int]
type Coords = tuple[Coord, ...]
type Algo = set[int]
type Grid = set[Coord]
type Size = tuple[range, range]

MASK = 2**9 - 1


def parse(s: str) -> tuple[Algo, Grid]:
    algo_str, image = s.split('\n\n')
    algo = {i for i, ch in enumerate(algo_str) if ch == '#'}
    return algo, {
        (i, j)
        for i, line in enumerate(image.splitlines())
        for j, ch in enumerate(line)
        if ch == '#'
    }


@cache
def around(c: Coord) -> Coords:
    i, j = c
    return tuple(product(range(i - 1, i + 2), range(j - 1, j + 2)))


def coord_to_bin(c: Coord, grid: Grid, *, flip: bool = False) -> int:
    n = 0
    for c2 in around(c):
        n = n * 2 + ((c2 in grid) ^ flip)
    return n


def widen(size: Size) -> Size:
    ii, jj = size
    ii_2 = range(ii.start - 1, ii.stop + 1)
    jj_2 = range(jj.start - 1, jj.stop + 1)
    return ii_2, jj_2


def apply(algo: Algo, grid: Grid, times: int = 1) -> Grid:
    def is_valid(c: Coord, *, flip: bool = False, invert: bool = False):
        return (coord_to_bin(c, grid, flip=flip) in algo) ^ invert

    i_min, j_min = map(min, zip(*grid))
    i_max, j_max = map(max, zip(*grid))
    size = range(i_min, i_max + 1), range(j_min, j_max + 1)
    for k in range(times):
        size = widen(size)
        flip = 0 in algo and k % 2 != 0
        invert = 0 in algo and k % 2 == 0
        grid = {
            c for c in product(*size) if is_valid(c, flip=flip, invert=invert)
        }
    return grid


def solve() -> tuple[int, int]:
    algo, grid = parse(read_puzzle())
    return len(apply(algo, grid, 2)), len(apply(algo, grid, 50))


if __name__ == '__main__':
    print(solve())
