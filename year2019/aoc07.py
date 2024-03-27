from itertools import permutations
from math import inf

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


def run_amplifiers(
    program: Intcode, phases: tuple[int, ...], initial_input=0
) -> int:
    output = initial_input
    for i in range(5):
        gen = iter(Computer(program))
        next(gen)
        gen.send(phases[i])
        output = gen.send(output)
    return output


def find_max_output(program: Intcode, *, use_loop=False):
    max_output = -inf
    run = run_amplifiers_loop if use_loop else run_amplifiers
    phase_range = range(5, 10) if use_loop else range(5)
    for phases in permutations(phase_range):
        output = run(program, phases)
        if output > max_output:
            max_output = output
    return max_output


def run_amplifiers_loop(
    program: Intcode, phases: tuple[int, ...], initial_input=0
) -> int:
    output = initial_input
    gens = [iter(Computer(program)) for _ in range(5)]
    for i in range(5):
        next(gens[i])
        gens[i].send(phases[i])
    while True:
        for i in range(5):
            try:
                output = gens[i].send(output)
                next(gens[i])
            except StopIteration:
                if i == 4:
                    return output


def solve():
    program = parse(read_puzzle())
    return find_max_output(program), find_max_output(program, use_loop=True)


if __name__ == '__main__':
    print(solve())
