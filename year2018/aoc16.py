import operator
import re
from typing import Dict, List, Tuple

from helpers import read_puzzle

Tuple4 = Tuple[int, ...]
Sample = Tuple[Tuple4, Tuple4, Tuple4]


def parse(s: str) -> Tuple[List[Sample], List[Tuple4]]:
    group_n = lambda iterable, n: list(zip(*([iter(iterable)] * n)))
    s1, s2 = s.split('\n\n\n\n')
    numbers1 = map(int, re.findall(r'\d+', s1))  # find all numbers
    numbers2 = map(int, re.findall(r'\d+', s2))  # find all numbers
    # noinspection PyTypeChecker
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
    'setr': (('r', 'i'), lambda x, y: x),
    'seti': (('i', 'i'), lambda x, y: x),
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
    reg = list(reg)
    reg[c] = func(a_val, b_val)
    return tuple(reg)


def matches(reg_before: Tuple4, op: Tuple4, reg_after: Tuple4) -> List[int]:
    regs = ((n, execute((n, *op[1:]), reg_before))
            for n in range(len(opcodes)))
    return [n for n, reg in regs if reg == reg_after]


def count_more_than_3(samples: List[Sample]) -> int:
    return sum(int(len(matches(*sample)) >= 3) for sample in samples)


def decode_and_run(samples: List[Sample], program: List[Tuple4]) -> int:
    x_to_op_num: Dict[int, int] = {}
    cache: Dict[Sample, List[int]] = {}
    while len(x_to_op_num) < len(opcodes):
        for sample in samples:
            if sample not in cache:
                cache[sample] = matches(*sample)
                continue
            x = sample[1][0]
            if x in x_to_op_num:  # already decoded
                continue
            # Remove op_nums that have already been matched to other xs
            cache[sample] = [op_num for op_num in cache[sample]
                             if op_num not in x_to_op_num.values()]
            if len(cache[sample]) == 1:
                x_to_op_num[x] = cache[sample][0]  # decode
                continue
    reg = (0, 0, 0, 0)
    for op in program:
        op = (x_to_op_num[op[0]], *op[1:])
        reg = execute(op, reg)
    return reg[0]


def solve():
    samples, program = parse(read_puzzle())
    return count_more_than_3(samples), decode_and_run(samples, program)


if __name__ == '__main__':
    print(solve())
