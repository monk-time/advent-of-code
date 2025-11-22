# https://adventofcode.com/2019/day/9

from intcode import Computer, Intcode, parse
from utils_proxy import read_puzzle


def boost(program: Intcode, input_val: int) -> int:
    gen = iter(Computer(program))
    next(gen)
    return gen.send(input_val)


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    return boost(puzzle, 1), boost(puzzle, 2)


if __name__ == '__main__':
    print(solve())
