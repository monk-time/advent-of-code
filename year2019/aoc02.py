from itertools import product

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split(',')]


Intcode = list[int]


def run_intcode(program: Intcode) -> Intcode:
    """Execute the Intcode program. Mutates the program."""
    i = 0  # position in the program to execute
    while True:
        match program[i]:
            case 1:
                a, b, c = program[i + 1 : i + 4]
                program[c] = program[a] + program[b]
            case 2:
                a, b, c = program[i + 1 : i + 4]
                program[c] = program[a] * program[b]
            case 99:
                return program
            case _:
                raise Exception(f'An unknown opcode {program[i]}')
        i += 4


def init(program: Intcode, noun: int, verb: int) -> Intcode:
    return [program[0], noun, verb, *program[3:]]


def find_input(program):
    noun, verb = 0, 0  # PyCharm complains without this line
    for noun, verb in product(range(100), repeat=2):
        output = run_intcode(init(program, noun, verb))[0]
        if output == 19690720:
            break
    return 100 * noun + verb


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    part1 = run_intcode(init(puzzle, 12, 2))[0]
    part2 = find_input(puzzle)
    return part1, part2


if __name__ == '__main__':
    print(solve())
