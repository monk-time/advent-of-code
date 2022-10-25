from typing import Iterable

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split(',')]


Intcode = list[int]


def nth_digit(n: int, pos: int) -> int:
    return n // (10 ** (pos - 1)) % 10


def get_parameters(program, i):
    a, b = program[i + 1:i + 3]
    if nth_digit(program[i], 3) == 0:
        a = program[a]
    if nth_digit(program[i], 4) == 0:
        b = program[b]
    return a, b


def run_intcode(program: Intcode, input_value: int = 0) -> Iterable[int]:
    """Execute the Intcode program."""
    i = 0  # position in the program to execute
    program = program[:]
    while True:
        op = program[i] % 100
        match op:
            case 1 | 2:  # add, multiply
                a, b = get_parameters(program, i)
                c = program[i + 3]
                if op == 1:
                    program[c] = a + b
                else:
                    program[c] = a * b
                i += 4
            case 3:  # input
                program[program[i + 1]] = input_value
                i += 2
            case 4:  # output
                a = program[i + 1]
                if nth_digit(program[i], 3) == 0:
                    a = program[a]
                yield a
                i += 2
            case 5:  # jump-if-true
                a, b = get_parameters(program, i)
                i = b if a else i + 3
            case 6:  # jump-if-false
                a, b = get_parameters(program, i)
                i = b if not a else i + 3
            case 7:  # less than
                a, b = get_parameters(program, i)
                program[program[i + 3]] = 1 if a < b else 0
                i += 4
            case 8:  # equals
                a, b = get_parameters(program, i)
                program[program[i + 3]] = 1 if a == b else 0
                i += 4
            case 99:
                return
            case _:
                raise Exception(f'An unknown opcode {op} at {i=}')


def solve():
    puzzle = parse(read_puzzle())
    part1 = list(run_intcode(puzzle, 1))[-1]
    part2 = list(run_intcode(puzzle, 5))[-1]
    return part1, part2


if __name__ == '__main__':
    print(solve())
