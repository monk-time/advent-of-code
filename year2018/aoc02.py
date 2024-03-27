from collections import Counter
from collections.abc import Iterable
from itertools import combinations

from helpers import read_puzzle


def has_exactly_n_of_any_letter(box_id: str, n: int) -> bool:
    return n in Counter(box_id).values()


def checksum(box_ids: Iterable[str]) -> int:
    def count(n: int):
        return sum(
            has_exactly_n_of_any_letter(box_id, n) for box_id in box_ids
        )

    return count(2) * count(3)


def matching_letters(box_a: str, box_b: str) -> str:
    return ''.join(a for (a, b) in zip(box_a, box_b) if a == b)


def is_correct_pair(box_a: str, box_b: str) -> bool:
    """Two IDs are correct if they differ by exactly one character at the same position."""
    return len(matching_letters(box_a, box_b)) == len(box_a) - 1


def part2(box_ids: Iterable[str]) -> str:
    matching_pair = next(
        t for t in combinations(box_ids, 2) if is_correct_pair(*t)
    )
    return matching_letters(*matching_pair)


def solve():
    puzzle = read_puzzle().splitlines()
    return checksum(puzzle), part2(puzzle)


if __name__ == '__main__':
    print(solve())
