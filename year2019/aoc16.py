# https://adventofcode.com/2019/day/16

from itertools import accumulate, chain, cycle, islice, repeat, starmap
from operator import mul

from helpers import read_puzzle, timed

PATTERN = (0, 1, 0, -1)

Signal = tuple[int, ...]


def parse(s: str) -> Signal:
    return tuple(int(ch) for ch in s)


def to_str(signal: Signal) -> str:
    return ''.join(map(str, signal))


def pattern(length: int, times: int) -> Signal:
    repeated = (repeat(n, times) for n in PATTERN)
    looped = cycle(chain.from_iterable(repeated))
    return tuple(islice(looped, 1, length + 1))


def get_patterns(length: int) -> tuple[Signal, ...]:
    return tuple(pattern(length, i) for i in range(1, length + 1))


def apply_phase_of_fft(signal: Signal, patterns: tuple[Signal, ...]) -> Signal:
    n = len(signal)
    apply_pattern = lambda i: starmap(mul, zip(signal[i:], patterns[i][i:]))
    get_digit = lambda i: abs(sum(apply_pattern(i))) % 10
    return tuple(get_digit(i) for i in range(n))


def apply_n_phases(signal: Signal, n: int) -> Signal:
    patterns = get_patterns(len(signal))
    for _ in range(n):
        signal = apply_phase_of_fft(signal, patterns)
    return signal[:8]


def real_signal(signal: Signal) -> Signal:
    input_signal = signal * 10_000
    offset = int(to_str(signal[:7]))
    next_signal = reversed(input_signal[offset:])
    for _ in range(100):
        next_signal = accumulate(next_signal, lambda a, b: (a + b) % 10)
    return tuple(islice(reversed(tuple(next_signal)), 8))


@timed
def solve() -> tuple[str, str]:
    signal = parse(read_puzzle())
    part1 = to_str(apply_n_phases(signal, 100))
    part2 = to_str(real_signal(signal))
    return part1, part2


if __name__ == '__main__':
    print(solve())
