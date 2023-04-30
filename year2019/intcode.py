from collections import defaultdict

Intcode = list[int]


def parse(s: str) -> Intcode:
    return [int(line) for line in s.split(',')]


def nth_digit(n: int, pos: int) -> int:
    return n // (10 ** (pos - 1)) % 10


def get_parameters(program, i, count, rel_base):
    a = program[i + 1]
    match nth_digit(program[i], 3):
        case 0:
            a = program[a]
        case 2:
            a = program[a + rel_base]
    if count == 1:
        return a

    b = program[i + 2]
    match nth_digit(program[i], 4):
        case 0:
            b = program[b]
        case 2:
            b = program[b + rel_base]
    if count == 2:
        return a, b

    c = program[i + 3]
    match nth_digit(program[i], 5):
        case 2:
            c = c + rel_base
    return a, b, c


def run_intcode(program: Intcode):
    """Execute the Intcode program."""
    i = 0  # position in the program to execute
    program = defaultdict(lambda: 0, zip(range(len(program)), program))
    rel_base = 0
    print()
    while True:
        op = program[i] % 100
        match op:
            case 1 | 2:  # add, multiply
                a, b, c = get_parameters(program, i, 3, rel_base)
                if op == 1:
                    program[c] = a + b
                else:
                    program[c] = a * b
                i += 4
            case 3:  # input
                a = program[i + 1]
                if nth_digit(program[i], 3) == 2:
                    a += rel_base
                program[a] = yield
                i += 2
            case 4:  # output
                a = get_parameters(program, i, 1, rel_base)
                yield a
                i += 2
            case 5:  # jump-if-true
                a, b = get_parameters(program, i, 2, rel_base)
                i = b if a else i + 3
            case 6:  # jump-if-false
                a, b = get_parameters(program, i, 2, rel_base)
                i = b if not a else i + 3
            case 7:  # less than
                a, b, c = get_parameters(program, i, 3, rel_base)
                program[c] = 1 if a < b else 0
                i += 4
            case 8:  # equals
                a, b, c = get_parameters(program, i, 3, rel_base)
                program[c] = 1 if a == b else 0
                i += 4
            case 9:  # relative base offset
                a = get_parameters(program, i, 1, rel_base)
                rel_base += a
                i += 2
            case 99:
                return
            case _:
                raise Exception(f'An unknown opcode {op} at {i=}')
