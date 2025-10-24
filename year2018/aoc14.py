# https://adventofcode.com/2018/day/14


from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable


def scoreboard() -> Iterable[tuple[list[int], int]]:
    board = [3, 7]
    elf_a, elf_b = 0, 1
    while True:
        cur_a, cur_b = board[elf_a], board[elf_b]
        total = cur_a + cur_b
        board += divmod(total, 10) if total >= 10 else (total,)
        yield board, total
        elf_a = (elf_a + cur_a + 1) % len(board)
        elf_b = (elf_b + cur_b + 1) % len(board)


def improve(num: int) -> str | None:
    for board, _ in scoreboard():
        if len(board) >= num + 10:
            return ''.join(map(str, board[num : num + 10]))
    return None


def recipes_to_the_left(s: str) -> int | None:
    target, t = list(map(int, s)), len(s)
    for board, total in scoreboard():
        if total >= 10 and board[-t - 1 : -1] == target:
            return len(board) - t - 1
        if board[-t:] == target:
            return len(board) - t
    return None


def solve():
    puzzle = read_puzzle()
    return improve(int(puzzle)), recipes_to_the_left(puzzle)


if __name__ == '__main__':
    print(solve())
