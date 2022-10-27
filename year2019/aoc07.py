from itertools import permutations
from math import inf

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


def run_intcode(program: Intcode, phase: int, input_value: int) -> int:
    """Execute the Intcode program."""
    i = 0  # position in the program to execute
    program = program[:]
    consumed_inputs = 0
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
                match consumed_inputs:
                    case 0:
                        program[program[i + 1]] = phase
                    case 1:
                        program[program[i + 1]] = input_value
                    case _:
                        raise Exception('A program is expected to receive only two inputs')
                consumed_inputs += 1
                i += 2
            case 4:  # output
                a = program[i + 1]
                if nth_digit(program[i], 3) == 0:
                    a = program[a]
                i += 2
                return a
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
                raise Exception(f'A program should return a value instead of exiting')
            case _:
                raise Exception(f'An unknown opcode {op} at {i=}')


def run_amplifiers(program: Intcode, phases: tuple[int, ...], initial_input=0) -> int:
    output = run_intcode(program, phases[0], initial_input)
    output = run_intcode(program, phases[1], output)
    output = run_intcode(program, phases[2], output)
    output = run_intcode(program, phases[3], output)
    output = run_intcode(program, phases[4], output)
    return output


def find_max_output(program: Intcode):
    max_output = -inf
    for phases in permutations(range(5)):
        output = run_amplifiers(program, phases)
        if output > max_output:
            print(f'New maximum {output=} with {phases=}')
            max_output = output
    return max_output


def feedback_loop(program: Intcode):
    max_output = -inf
    initial_input = 0
    for phases in permutations(range(5, 10)):
        while True:
            initial_input = run_amplifiers(program, phases, initial_input)
        if output > max_output:
            print(f'New maximum {output=} with {phases=}')
            max_output = output
    return max_output


def solve():
    program = parse(read_puzzle())
    part1 = find_max_output(program)
    return find_max_output(program), feedback_loop(program)


if __name__ == '__main__':
    print(solve())
