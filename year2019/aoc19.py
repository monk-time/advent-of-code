# https://adventofcode.com/2019/day/19

from bisect import bisect_left
from itertools import product
from typing import TYPE_CHECKING

from helpers import read_puzzle
from intcode import Computer, Intcode, parse

if TYPE_CHECKING:
    from collections.abc import Callable

type Coord = tuple[int, int]


def get_point(program: Intcode, x: int, y: int) -> int:
    gen = iter(Computer(program))
    next(gen)
    gen.send(x)
    return gen.send(y)


def count_points(program: Intcode) -> int:
    total, ray_start_x = 0, 0
    for y in range(50):
        seen_a_point = False
        for x in range(ray_start_x, 50):
            value = get_point(program, x, y)
            total += value
            if value == 1 and not seen_a_point:
                seen_a_point = True
                ray_start_x = x
            if value == 0 and seen_a_point:
                break
    return total


def calc_angles(program: Intcode) -> tuple[float, float]:
    y = 100000  # arbitrary point far enough to provide enough precision
    # Find any point inside of the beam
    mid = next(x for x in range(0, y * 4, 1000) if get_point(program, x, y))
    x1_key: Callable[[int], int] = lambda x: get_point(program, x, y)
    x1 = bisect_left(range(mid * 2), 1, hi=mid, key=x1_key)
    x2_key: Callable[[int], int] = lambda x: -get_point(program, x, y)
    x2 = bisect_left(range(mid * 2), 0, lo=mid, key=x2_key)
    return y / x1, y / x2


def fit_in_ray(program: Intcode) -> int:
    a, b = calc_angles(program)
    # Trig magic to find the required point
    x = round(99 * (b + 1) / (a - b))
    y = round(99 * (b + b * a) / (a - b))
    # Check around to compensate for lost precision
    delta = 5
    pos = next(
        (x + dx, y + dy)
        for dx, dy in product(range(-delta, delta + 1), repeat=2)
        if get_point(program, x + dx + 99, y + dy)
        == get_point(program, x + dx, y + dy + 99)
        == 1
    )
    return 10000 * pos[0] + pos[1]


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    return count_points(program), fit_in_ray(program)


if __name__ == '__main__':
    print(solve())
