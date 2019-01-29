from collections import deque

from helpers import read_puzzle


def improve(steps: int) -> str:
    board = [3, 7]
    elf_a, elf_b = 0, 1
    while len(board) < steps + 10:
        cur_a, cur_b = board[elf_a], board[elf_b]
        for c in str(cur_a + cur_b):
            board.append(int(c))
        elf_a = (elf_a + cur_a + 1) % len(board)
        elf_b = (elf_b + cur_b + 1) % len(board)
    return ''.join(map(str, board[steps:steps + 10]))


def recipes_to_the_left(scores: str) -> int:
    board = [3, 7]
    elf_a, elf_b = 0, 1
    scores = deque(int(c) for c in scores)
    tail = deque(board, maxlen=len(scores))
    while tail != scores:
        cur_a, cur_b = board[elf_a], board[elf_b]
        for c in str(cur_a + cur_b):
            board.append(int(c))
            tail.append(int(c))
            if tail == scores:  # can happen when the sum of scores is >= 10
                break
        elf_a = (elf_a + cur_a + 1) % len(board)
        elf_b = (elf_b + cur_b + 1) % len(board)
    return len(board) - len(scores)


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(improve(int(puzzle)))
    print(recipes_to_the_left(puzzle))
    # < 150718217
