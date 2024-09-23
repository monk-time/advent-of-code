# https://adventofcode.com/2020/day/2

import re
from collections import Counter
from dataclasses import dataclass
from typing import Self

from helpers import read_puzzle

pattern = re.compile(r'^(?P<x>\d+)-(?P<y>\d+) (?P<char>\w): (?P<pwd>\w+)$')


@dataclass
class Entry:
    x: int
    y: int
    char: str
    pwd: str

    def __post_init__(self):
        self.x = int(self.x)
        self.y = int(self.y)

    @classmethod
    def from_str(cls, line: str) -> Self:
        if match := pattern.match(line):
            return cls(**match.groupdict())  # type: ignore
        raise ValueError


def parse(s: str) -> list[Entry]:
    return [Entry.from_str(line) for line in s.split('\n')]


def solve() -> tuple[int, int]:
    entries = parse(read_puzzle())
    is_valid_1 = lambda e: e.x <= Counter(e.pwd)[e.char] <= e.y
    is_valid_2 = lambda e: (e.pwd[e.x - 1], e.pwd[e.y - 1]).count(e.char) == 1
    return (sum(map(is_valid_1, entries)), sum(map(is_valid_2, entries)))


if __name__ == '__main__':
    print(solve())
