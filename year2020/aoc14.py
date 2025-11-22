# https://adventofcode.com/2020/day/14

import re
from collections.abc import Iterable

from utils_proxy import read_puzzle

RE_MASK = re.compile(r'^mask = (?P<mask>[10X]+)$')
RE_MEM = re.compile(r'^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$')

BITS = 36

type Program = Iterable[str | tuple[int, int]]


def parse(s: str) -> Program:
    for line in s.split('\n'):
        if m := RE_MASK.match(line):
            yield m.group('mask')
        if m := RE_MEM.match(line):
            yield (int(m.group('addr')), int(m.group('val')))


def to_bin_arr(n: int, length: int = BITS) -> list[str]:
    return list(f'{n:0>{length}b}')


def run(program: Program) -> int:
    mem: dict[int, int] = {}
    for command in program:
        match command:
            case str(mask):
                pass
            case (addr, val):
                val_bin = to_bin_arr(val)
                for i, ch in enumerate(mask):  # type: ignore
                    if ch != 'X':
                        val_bin[i] = ch
                mem[addr] = int(''.join(val_bin), base=2)
    return sum(mem.values())


def run_v2(program: Program) -> int:
    holes: tuple[int, ...] = ()
    mem: dict[int, int] = {}
    for command in program:
        match command:
            case str(mask):
                holes = tuple(i for i, ch in enumerate(mask) if ch == 'X')
            case (addr, val):
                addr_bin = to_bin_arr(addr)
                for i, ch in enumerate(mask):  # type: ignore
                    if ch == '1':
                        addr_bin[i] = ch
                bits = len(holes)
                for fill_val in range(2**bits):
                    fill_bin = to_bin_arr(fill_val, bits)
                    for i, ch in zip(holes, fill_bin):
                        addr_bin[i] = ch
                    mem[int(''.join(addr_bin), base=2)] = val
    return sum(mem.values())


def solve() -> tuple[int, int]:
    program = list(parse(read_puzzle()))
    return run(program), run_v2(program)


if __name__ == '__main__':
    print(solve())
