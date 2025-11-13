# https://adventofcode.com/2018/day/16

import operator
import re
from itertools import batched
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

type Tuple4 = tuple[int, ...]
type Sample = tuple[Tuple4, Tuple4, Tuple4]


def parse(s: str) -> tuple[list[Sample], list[Tuple4]]:
    s1, s2 = s.split('\n\n\n\n')
    numbers1 = map(int, re.findall(r'\d+', s1))  # find all numbers
    numbers2 = map(int, re.findall(r'\d+', s2))  # find all numbers
    g4_1: Iterable[Tuple4] = batched(numbers1, 4, strict=True)
    g4_2: Iterable[Tuple4] = batched(numbers2, 4, strict=True)
    return list(batched(g4_1, 3, strict=True)), list(g4_2)  # type: ignore


op_library: dict[str, tuple[tuple[str, str], Callable[[int, int], int]]] = {
    'addr': (('r', 'r'), operator.add),
    'addi': (('r', 'i'), operator.add),
    'mulr': (('r', 'r'), operator.mul),
    'muli': (('r', 'i'), operator.mul),
    'banr': (('r', 'r'), operator.and_),
    'bani': (('r', 'i'), operator.and_),
    'borr': (('r', 'r'), operator.or_),
    'bori': (('r', 'i'), operator.or_),
    'setr': (('r', 'i'), lambda x, _y: x),
    'seti': (('i', 'i'), lambda x, _y: x),
    'gtir': (('i', 'r'), lambda x, y: int(x > y)),
    'gtri': (('r', 'i'), lambda x, y: int(x > y)),
    'gtrr': (('r', 'r'), lambda x, y: int(x > y)),
    'eqir': (('i', 'r'), lambda x, y: int(x == y)),
    'eqri': (('r', 'i'), lambda x, y: int(x == y)),
    'eqrr': (('r', 'r'), lambda x, y: int(x == y)),
}

opcodes = list(op_library.keys())


def execute(instr: Tuple4, reg: Tuple4) -> Tuple4:
    n, a, b, c = instr
    (a_type, b_type), func = op_library[opcodes[n]]
    a_val = reg[a] if a_type == 'r' else a
    b_val = reg[b] if b_type == 'r' else b
    mut_reg = list(reg)
    mut_reg[c] = func(a_val, b_val)
    return tuple(mut_reg)


def matches(reg_before: Tuple4, op: Tuple4, reg_after: Tuple4) -> list[int]:
    regs = (
        (n, execute((n, *op[1:]), reg_before)) for n in range(len(opcodes))
    )
    return [n for n, reg in regs if reg == reg_after]


def count_more_than_3(samples: list[Sample]) -> int:
    return sum(int(len(matches(*sample)) >= 3) for sample in samples)


def decode_and_run(samples: list[Sample], program: list[Tuple4]) -> int:
    x_to_op_num: dict[int, int] = {}
    cache: dict[Sample, list[int]] = {}
    while len(x_to_op_num) < len(opcodes):
        for sample in samples:
            if sample not in cache:
                cache[sample] = matches(*sample)
                continue
            x = sample[1][0]
            if x in x_to_op_num:  # already decoded
                continue
            # Remove op_nums that have already been matched to other xs
            cache[sample] = [
                op_num
                for op_num in cache[sample]
                if op_num not in x_to_op_num.values()
            ]
            if len(cache[sample]) == 1:
                x_to_op_num[x] = cache[sample][0]  # decode
                continue
    reg = (0, 0, 0, 0)
    for op in program:
        decoded_op = (x_to_op_num[op[0]], *op[1:])
        reg = execute(decoded_op, reg)
    return reg[0]


def solve():
    samples, program = parse(read_puzzle())
    return count_more_than_3(samples), decode_and_run(samples, program)


if __name__ == '__main__':
    print(solve())
