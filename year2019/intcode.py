from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass

Intcode = list[int]


class UnknownOpCodeError(Exception):
    pass


def parse(s: str) -> Intcode:
    return [int(line) for line in s.split(',')]


def nth_digit(n: int, pos: int) -> int:
    return n // (10 ** (pos - 1)) % 10


@dataclass
class Computer:
    program: Intcode | defaultdict[int, int]
    pointer: int = 0
    rel_base: int = 0

    def __post_init__(self):
        if isinstance(self.program, defaultdict):
            self.program = self.program.copy()
        else:
            self.program = defaultdict(lambda: 0, enumerate(self.program))

    def __iter__(self) -> Generator[int, int]:
        """Execute the Intcode program.

        Raises:
            UnknownOpCodeError: if encountered an unknown op code
        """
        while True:
            op = self.program[self.pointer] % 100
            match op:
                case 1 | 2:  # add, multiply
                    a, b, c = self.get_parameters(3)  # type: ignore
                    self.program[c] = a + b if op == 1 else a * b
                    self.pointer += 4
                case 3:  # input
                    a = self.program[self.pointer + 1]
                    if nth_digit(self.program[self.pointer], 3) == 2:
                        a += self.rel_base
                    self.pointer += 2
                    self.program[a] = yield  # type: ignore
                case 4:  # output
                    a: int = self.get_parameters(1)  # type: ignore
                    self.pointer += 2
                    yield a
                case 5 | 6:  # jump-if-true, jump-if-false
                    a, b = self.get_parameters(2)  # type: ignore
                    cond = a if op == 5 else not a
                    self.pointer = b if cond else self.pointer + 3
                case 7 | 8:  # less than, equals
                    a, b, c = self.get_parameters(3)  # type: ignore
                    cond = a < b if op == 7 else a == b
                    self.program[c] = 1 if cond else 0
                    self.pointer += 4
                case 9:  # relative base offset
                    a: int = self.get_parameters(1)  # type: ignore
                    self.rel_base += a
                    self.pointer += 2
                case 99:
                    return
                case _:
                    msg = f'Unknown opcode {op} at {self.pointer=}'
                    raise UnknownOpCodeError(msg)

    def get_parameters(
        self, count: int
    ) -> int | tuple[int, int] | tuple[int, int, int]:
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
                c += self.rel_base
        return a, b, c
