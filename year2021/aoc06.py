# https://adventofcode.com/2021/day/6
# tags: #frequency #exponential-growth

from utils_proxy import read_puzzle


def parse(s: str) -> tuple[int, ...]:
    return tuple(int(x) for x in s.split(','))


def grow(nums: tuple[int, ...], days: int):
    counter = [nums.count(i) for i in range(9)]
    for _ in range(days):
        counter = counter[1:] + counter[:1]
        counter[6] += counter[-1]
    return sum(counter)


def solve() -> tuple[int, int]:
    nums = parse(read_puzzle())
    return grow(nums, 80), grow(nums, 256)


if __name__ == '__main__':
    print(solve())
