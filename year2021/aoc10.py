# https://adventofcode.com/2021/day/10
# tags: #brackets

from functools import reduce
from typing import TYPE_CHECKING, Literal, TypedDict

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
SYNTAX_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORES = {')': 1, ']': 2, '}': 3, '>': 4}


class Result(TypedDict):
    type: Literal['corrupted', 'incomplete']
    data: str


def parse(s: str) -> list[str]:
    return s.splitlines()


def check_brackets(line: str) -> Result:
    expected_ends: list[str] = []
    for ch in line:
        if ch in {'(', '[', '{', '<'}:
            expected_ends.append(PAIRS[ch])
            continue
        if not expected_ends:
            return Result(type='corrupted', data=ch)
        if ch != expected_ends.pop():
            return Result(type='corrupted', data=ch)
    data = ''.join(reversed(expected_ends))
    return Result(type='incomplete', data=data)


def syntax_score(results: Iterable[Result]) -> int:
    return sum(
        SYNTAX_SCORES[r['data']] for r in results if r['type'] == 'corrupted'
    )


def completion_score(results: Iterable[Result]) -> int:
    scores = [
        reduce(lambda acc, ch: acc * 5 + COMPLETION_SCORES[ch], r['data'], 0)
        for r in results
        if r['type'] == 'incomplete'
    ]
    return sorted(scores)[len(scores) // 2]


def solve() -> tuple[int, int]:
    lines = parse(read_puzzle())
    results = [check_brackets(line) for line in lines]
    return syntax_score(results), completion_score(results)


if __name__ == '__main__':
    print(solve())
