from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split(',')]


Intcode = list[int]


def run_intcode(program: Intcode) -> Intcode:
    program = program[:]  # mutate only the copy of the program
    i = 0  # position in the program to execute
    while True:
        match program[i]:
            case 1:
                a, b, c = program[i + 1:i + 4]
                program[c] = program[a] + program[b]
            case 2:
                a, b, c = program[i + 1:i + 4]
                program[c] = program[a] * program[b]
            case 99:
                return program
            case _:
                raise Exception(f'An unknown opcode {program[i]}')
        i += 4


def prerun(program: Intcode) -> Intcode:
    return [program[0], 12, 2, *program[3:]]


def solve():
    puzzle = parse(read_puzzle())
    part1 = run_intcode(prerun(puzzle))[0]
    return part1, None


if __name__ == '__main__':
    print(solve())
