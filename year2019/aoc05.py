from helpers import read_puzzle
from intcode import Computer, Intcode, parse


def run_with_input(program: Intcode, value: int):
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
