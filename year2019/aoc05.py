# https://adventofcode.com/2019/day/5


from typing import TYPE_CHECKING

from helpers import read_puzzle
from intcode import Computer, Intcode, parse

if TYPE_CHECKING:
    from collections.abc import Iterable


def run_with_input(program: Intcode, value: int) -> Iterable[int]:
    gen = iter(Computer(program))
    next(gen)
    yield gen.send(value)
    yield from gen


def solve():
    program = parse(read_puzzle())
    part1 = list(run_with_input(program, 1))[-1]
    part2 = list(run_with_input(program, 5))[-1]
    return part1, part2


if __name__ == '__main__':
    print(solve())
