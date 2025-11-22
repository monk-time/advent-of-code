# https://adventofcode.com/2020/day/8

from dataclasses import dataclass

from utils_proxy import read_puzzle

type Program = list[tuple[str, int]]


@dataclass(frozen=True)
class Result:
    acc: int
    inf_loop: bool


def parse(s: str) -> Program:
    return [((a := line.split())[0], int(a[1])) for line in s.split('\n')]


def run(program: Program) -> Result:
    pointer, acc = 0, 0
    visited: set[int] = set()
    while pointer not in visited and pointer < len(program):
        visited.add(pointer)
        match program[pointer]:
            case ('acc', n):
                acc += n
                pointer += 1
            case ('jmp', n):
                pointer += n
            case ('nop', _):
                pointer += 1
            case _:
                msg = 'Unexpected op'
                raise ValueError(msg)
    return Result(acc=acc, inf_loop=pointer < len(program))


def fix(program: Program) -> Result:
    flip = {'jmp': 'nop', 'nop': 'jmp'}
    for i in range(len(program)):
        cmd, n = program[i]
        if cmd == 'acc':
            continue
        program[i] = (flip[cmd], n)
        result = run(program)
        program[i] = (cmd, n)
        if not result.inf_loop:
            return result
    msg = 'Unfixable program'
    raise ValueError(msg)


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    return run(program).acc, fix(program).acc


if __name__ == '__main__':
    print(solve())
