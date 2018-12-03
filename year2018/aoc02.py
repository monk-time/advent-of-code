from collections import Counter
from itertools import combinations
from typing import Iterable

from helpers import read_puzzle


def has_exactly_n_of_any_letter(box_id: str, n: int) -> bool:
    return n in Counter(box_id).values()


def checksum(box_ids: Iterable[str]) -> int:
    twice = sum(has_exactly_n_of_any_letter(box_id, 2) for box_id in box_ids)
    thrice = sum(has_exactly_n_of_any_letter(box_id, 3) for box_id in box_ids)
    return twice * thrice


def matching_letters(box_a: str, box_b: str) -> str:
    return ''.join(a for (a, b) in zip(box_a, box_b) if a == b)


def is_correct_pair(box_a: str, box_b: str) -> bool:
    return len(matching_letters(box_a, box_b)) == len(box_a) - 1


def part2(box_ids: Iterable[str]) -> str:
    matching_pair = next(t for t in combinations(box_ids, 2) if is_correct_pair(*t))
    return matching_letters(*matching_pair)


if __name__ == '__main__':
    puzzle = read_puzzle().splitlines()
    print(checksum(puzzle))
    print(part2(puzzle))
