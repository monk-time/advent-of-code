from itertools import permutations
from math import inf

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split(',')]


Intcode = list[int]


class AmplifierHalt(Exception):
    pass


def nth_digit(n: int, pos: int) -> int:
    return n // (10 ** (pos - 1)) % 10


def get_parameters(program, i):
    a, b = program[i + 1:i + 3]
    if nth_digit(program[i], 3) == 0:
        a = program[a]
    if nth_digit(program[i], 4) == 0:
        b = program[b]
    return a, b


def run_intcode(program: Intcode):
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
                program[program[i + 1]] = yield
                i += 2
            case 4:  # output
                a = program[i + 1]
                if nth_digit(program[i], 3) == 0:
                    a = program[a]
                i += 2
                yield a
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
                raise AmplifierHalt
            case _:
                raise Exception(f'An unknown opcode {op} at {i=}')


def run_amplifiers(program: Intcode, phases: tuple[int, ...], initial_input=0) -> int:
    output = initial_input
    for i in range(5):
        gen = run_intcode(program)
        next(gen)
        gen.send(phases[i])
        output = gen.send(output)
    return output


def find_max_output(program: Intcode, use_loop=False):
    max_output = -inf
    run = run_amplifiers_loop if use_loop else run_amplifiers
    phase_range = range(5, 10) if use_loop else range(5)
    for phases in permutations(phase_range):
        output = run(program, phases)
        if output > max_output:
            max_output = output
    return max_output


def run_amplifiers_loop(program: Intcode, phases: tuple[int, ...], initial_input=0) -> int:
    output = initial_input
    gens = [run_intcode(program) for _ in range(5)]
    for i in range(5):
        next(gens[i])
        gens[i].send(phases[i])
    while True:
        for i in range(5):
            try:
                output = gens[i].send(output)
                next(gens[i])
            except AmplifierHalt:
                if i == 4:
                    return output


def solve():
    program = parse(read_puzzle())
    return find_max_output(program), find_max_output(program, use_loop=True)


if __name__ == '__main__':
    print(solve())
