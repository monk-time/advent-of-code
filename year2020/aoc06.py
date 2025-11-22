# https://adventofcode.com/2020/day/6

from collections import Counter

from utils_proxy import read_puzzle

type Groups = list[tuple[Counter[str], int]]


def parse(s: str) -> Groups:
    return [
        (Counter(group.replace('\n', '')), group.count('\n') + 1)
        for group in s.split('\n\n')
    ]


def count_questions_any(groups: Groups) -> int:
    return sum(len(counter) for counter, _ in groups)


def count_questions_all(groups: Groups) -> int:
    return sum(v == n for counter, n in groups for v in counter.values())


def solve() -> tuple[int, int]:
    groups = parse(read_puzzle())
    return count_questions_any(groups), count_questions_all(groups)


if __name__ == '__main__':
    print(solve())
