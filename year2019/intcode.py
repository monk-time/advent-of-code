from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:
    from collections.abc import Generator

type Intcode = list[int]


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
                    a, b, c = self.get_parameters(3)
                    self.program[c] = a + b if op == 1 else a * b
                    self.pointer += 4
                case 3:  # input
                    a = self.program[self.pointer + 1]
                    if nth_digit(self.program[self.pointer], 3) == 2:
                        a += self.rel_base
                    self.pointer += 2
                    self.program[a] = yield  # type: ignore
                case 4:  # output
                    a = self.get_parameters(1)
                    self.pointer += 2
                    yield a
                case 5 | 6:  # jump-if-true, jump-if-false
                    a, b = self.get_parameters(2)
                    cond = a if op == 5 else not a
                    self.pointer = b if cond else self.pointer + 3
                case 7 | 8:  # less than, equals
                    a, b, c = self.get_parameters(3)
                    cond = a < b if op == 7 else a == b
                    self.program[c] = 1 if cond else 0
                    self.pointer += 4
                case 9:  # relative base offset
                    a = self.get_parameters(1)
                    self.rel_base += a
                    self.pointer += 2
                case 99:
                    return
                case _:
                    msg = f'Unknown opcode {op} at {self.pointer=}'
                    raise UnknownOpCodeError(msg)

    @overload
    def get_parameters(self, count: Literal[1]) -> int: ...
    @overload
    def get_parameters(self, count: Literal[2]) -> tuple[int, int]: ...
    @overload
    def get_parameters(self, count: Literal[3]) -> tuple[int, int, int]: ...

    def get_parameters(
        self, count: int
    ) -> int | tuple[int, int] | tuple[int, int, int]:
        a = self.program[self.pointer + 1]
        digit_3 = nth_digit(self.program[self.pointer], 3)
        if digit_3 == 0:
            a = self.program[a]
        elif digit_3 == 2:
            a = self.program[a + self.rel_base]
        if count == 1:
            return a

        b = self.program[self.pointer + 2]
        digit_4 = nth_digit(self.program[self.pointer], 4)
        if digit_4 == 0:
            b = self.program[b]
        elif digit_4 == 2:
            b = self.program[b + self.rel_base]
        if count == 2:
            return a, b

        c = self.program[self.pointer + 3]
        digit_5 = nth_digit(self.program[self.pointer], 5)
        if digit_5 == 2:
            c += self.rel_base
        return a, b, c
