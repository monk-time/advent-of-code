# https://adventofcode.com/2020/day/25

from helpers import read_puzzle

MOD = 20201227


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def find_lsize(pub: int) -> int:
    n = loop_size = 1
    while (n := (n * 7) % MOD) != pub:
        loop_size += 1
    return loop_size


def get_enc_key(pub_card: int, pub_door: int) -> int:
    return pow(pub_door, find_lsize(pub_card), MOD)


def solve() -> tuple[int, int]:
    pub_card, pub_door = parse(read_puzzle())
    return get_enc_key(pub_card, pub_door), 0


if __name__ == '__main__':
    print(solve())
