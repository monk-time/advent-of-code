from collections import defaultdict
from dataclasses import dataclass
from typing import Generator

Intcode = list[int]


def parse(s: str) -> Intcode:
    return [int(line) for line in s.split(',')]


def nth_digit(n: int, pos: int) -> int:
    return n // (10 ** (pos - 1)) % 10


@dataclass
class Computer:
    program: Intcode
    pointer: int = 0
    rel_base: int = 0

    def __post_init__(self):
        self.program = defaultdict(lambda: 0, enumerate(self.program))

    def __iter__(self) -> Generator[int, int, None]:
        """Execute the Intcode program."""
        while True:
            op = self.program[self.pointer] % 100
            match op:
                case 1 | 2:  # add, multiply
                    a, b, c = self.get_parameters(3)
                    if op == 1:
                        self.program[c] = a + b
                    else:
                        self.program[c] = a * b
                    self.pointer += 4
                case 3:  # input
                    a = self.program[self.pointer + 1]
                    if nth_digit(self.program[self.pointer], 3) == 2:
                        a += self.rel_base
                    self.pointer += 2
                    self.program[a] = yield
                case 4:  # output
                    a = self.get_parameters(1)
                    self.pointer += 2
                    yield a
                case 5:  # jump-if-true
                    a, b = self.get_parameters(2)
                    self.pointer = b if a else self.pointer + 3
                case 6:  # jump-if-false
                    a, b = self.get_parameters(2)
                    self.pointer = b if not a else self.pointer + 3
                case 7:  # less than
                    a, b, c = self.get_parameters(3)
                    self.program[c] = 1 if a < b else 0
                    self.pointer += 4
                case 8:  # equals
                    a, b, c = self.get_parameters(3)
                    self.program[c] = 1 if a == b else 0
                    self.pointer += 4
                case 9:  # relative base offset
                    a = self.get_parameters(1)
                    self.rel_base += a
                    self.pointer += 2
                case 99:
                    return
                case _:
                    raise Exception(f'Unknown opcode {op} at {self.pointer=}')

    def get_parameters(self, count):
        a = self.program[self.pointer + 1]
        match nth_digit(self.program[self.pointer], 3):
            case 0:
                a = self.program[a]
            case 2:
                a = self.program[a + self.rel_base]
        if count == 1:
            return a

        b = self.program[self.pointer + 2]
        match nth_digit(self.program[self.pointer], 4):
            case 0:
                b = self.program[b]
            case 2:
                b = self.program[b + self.rel_base]
        if count == 2:
            return a, b

        c = self.program[self.pointer + 3]
        match nth_digit(self.program[self.pointer], 5):
            case 2:
                c = c + self.rel_base
        return a, b, c
