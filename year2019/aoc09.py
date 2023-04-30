from helpers import read_puzzle
from intcode import Intcode, parse, run_intcode


def boost(program: Intcode, input_val):
    gen = run_intcode(program)
    next(gen)
    return gen.send(input_val)


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    return boost(puzzle, 1), boost(puzzle, 2)


if __name__ == '__main__':
    print(solve())
