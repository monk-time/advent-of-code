# https://adventofcode.com/2021/day/8
# tags: #segmented-displays #decoding #frequency

import re
from collections import Counter
from itertools import chain
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

type Display = tuple[list[str], list[str]]


def parse(s: str) -> Generator[Display]:
    for line in s.splitlines():
        words = re.findall(r'\w+', line)
        yield words[:10], words[10:]


def count_easy(displays: Iterable[Display]) -> int:
    return sum(len(w) in {2, 3, 4, 7} for _, d in displays for w in d)


def get_freq_hashes(patterns: list[str], digits: list[str]) -> list[str]:
    c = Counter(chain(*patterns))
    return [''.join(sorted(str(c[x]) for x in digit)) for digit in digits]


DIGITS = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]

SCORE_TO_NUM = {
    score: str(i) for i, score in enumerate(get_freq_hashes(DIGITS, DIGITS))
}


def decode(display: Display) -> str:
    return ''.join(SCORE_TO_NUM[score] for score in get_freq_hashes(*display))


def decode_all(displays: Iterable[Display]) -> int:
    return sum(int(decode(display)) for display in displays)


def solve() -> tuple[int, int]:
    displays = list(parse(read_puzzle()))
    return count_easy(displays), decode_all(displays)


if __name__ == '__main__':
    print(solve())
