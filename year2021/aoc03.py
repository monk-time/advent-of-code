# https://adventofcode.com/2021/day/3
# tags: #binary #frequency

from typing import TYPE_CHECKING, Literal, cast

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

type Bit = Literal['0', '1']
type BitStr = list[Bit]
type Report = tuple[BitStr, ...]
type BitPosMap = dict[Bit, set[BitStr]]


def parse(s: str) -> Report:
    return cast('Report', tuple(s.splitlines()))


def index_by_bit_pos(report: Iterable[BitStr], i: int) -> BitPosMap:
    bit_pos_map: BitPosMap = {'0': set(), '1': set()}
    for s in report:
        bit_pos_map[s[i]].add(s)
    return bit_pos_map


def calc_power(report: Report) -> int:
    gamma, epsln = 0, 0
    for i in range(len(report[0])):
        b = index_by_bit_pos(report, i)
        gamma, epsln = gamma * 2, epsln * 2
        if len(b['0']) > len(b['1']):
            epsln += 1
        else:
            gamma += 1
    return gamma * epsln


def calc_rating(report: Report, comp_func: Callable[[int, int], bool]) -> int:
    matching = set(report)
    for i in range(len(report[0])):
        b = index_by_bit_pos(matching, i)
        matching &= b['0'] if comp_func(len(b['0']), len(b['1'])) else b['1']
        if len(matching) <= 1:
            break
    return int(''.join(next(iter(matching))), 2)


def calc_life_support(report: Report) -> int:
    o2 = calc_rating(report, int.__gt__)
    co2 = calc_rating(report, int.__le__)
    return o2 * co2


def solve() -> tuple[int, int]:
    report = parse(read_puzzle())
    return calc_power(report), calc_life_support(report)


if __name__ == '__main__':
    print(solve())
