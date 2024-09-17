# https://adventofcode.com/2019/day/21

from inspect import cleandoc

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


def find_hull_damage(program: Intcode, springscript: str) -> int:
    computer = Computer(program)
    gen = iter(computer)
    while next(gen) != 10:
        pass
    next(gen)
    for char in springscript:
        gen.send(ord(char))
    gen.send(10)
    line = ''
    try:
        while (output := next(gen)) <= 255:
            line += chr(output)
    except StopIteration:
        print(line)
        output = 0
    return output


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    # ^(A & B & C) & D - jump if any of the next three spots is empty
    springscript_walk = cleandoc("""
        OR A J
        AND B J
        AND C J
        NOT J J
        AND D J
        WALK
    """)
    # The same as previous but at least one of E and H should be solid
    springscript_run = cleandoc("""
        OR A J
        AND B J
        AND C J
        NOT J J
        AND D J
        OR E T
        OR H T
        AND T J
        RUN
    """)
    return (
        find_hull_damage(program, springscript_walk),
        find_hull_damage(program, springscript_run),
    )


if __name__ == '__main__':
    print(solve())
