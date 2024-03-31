# https://adventofcode.com/2018/day/16

import operator
import re

from helpers import read_puzzle

tuple4 = tuple[int, ...]
Sample = tuple[tuple4, tuple4, tuple4]


def parse(s: str) -> tuple[list[Sample], list[tuple4]]:
    group_n = lambda iterable, n: list(zip(*([iter(iterable)] * n)))
    s1, s2 = s.split('\n\n\n\n')
    numbers1 = map(int, re.findall(r'\d+', s1))  # find all numbers
    numbers2 = map(int, re.findall(r'\d+', s2))  # find all numbers
    return group_n(group_n(numbers1, 4), 3), group_n(numbers2, 4)


op_library = {
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


def execute(instr: tuple4, reg: tuple4) -> tuple4:
    n, a, b, c = instr
    (a_type, b_type), func = op_library[opcodes[n]]
    a_val = reg[a] if a_type == 'r' else a
    b_val = reg[b] if b_type == 'r' else b
    mut_reg = list(reg)
    mut_reg[c] = func(a_val, b_val)
    return tuple(mut_reg)


def matches(reg_before: tuple4, op: tuple4, reg_after: tuple4) -> list[int]:
    regs = (
        (n, execute((n, *op[1:]), reg_before)) for n in range(len(opcodes))
    )
    return [n for n, reg in regs if reg == reg_after]


def count_more_than_3(samples: list[Sample]) -> int:
    return sum(int(len(matches(*sample)) >= 3) for sample in samples)


def decode_and_run(samples: list[Sample], program: list[tuple4]) -> int:
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
