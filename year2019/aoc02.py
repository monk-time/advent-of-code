# https://adventofcode.com/2019/day/2

from itertools import product

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


def init(program: Intcode, noun: int, verb: int) -> Intcode:
    return [program[0], noun, verb, *program[3:]]


def get_output(program: Intcode) -> int:
    comp = Computer(program)
    for _ in comp:
        pass
    return comp.program[0]


def find_input(program):
    noun, verb = 0, 0  # PyCharm complains without this line
    for noun, verb in product(range(100), repeat=2):
        if get_output(init(program, noun, verb)) == 19690720:
            break
    return 100 * noun + verb


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    part1 = get_output(init(puzzle, 12, 2))
    part2 = find_input(puzzle)
    return part1, part2


if __name__ == '__main__':
    print(solve())
