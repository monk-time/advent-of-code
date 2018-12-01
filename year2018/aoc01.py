from itertools import cycle
from typing import Iterable

from year2018.helpers import read_puzzle


def parse(seq: str) -> Iterable[int]:
    sep = ', ' if ', ' in seq else '\n'
    return (int(s) for s in seq.split(sep))


def calibrate(seq: str, start_freq: int = 0) -> int:
    return sum(parse(seq), start_freq)


def calibrate_until_repeat(seq: str) -> int:
    visited, freq = {0}, 0
    for change in cycle(parse(seq)):
        freq += change
        if freq in visited:
            return freq
        visited.add(freq)


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(calibrate(puzzle))
    print(calibrate_until_repeat(puzzle))
