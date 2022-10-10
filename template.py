from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def solve():
    puzzle = parse(read_puzzle())
    return puzzle


if __name__ == '__main__':
    print(solve())
