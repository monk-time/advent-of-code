from itertools import chain, cycle, islice, repeat, starmap
from operator import mul
from helpers import read_puzzle

PATTERN = (0, 1, 0, -1)

Signal = tuple[int]


def parse(s: str) -> Signal:
    return tuple(int(ch) for ch in s)


def to_str(signal: Signal) -> str:
    return ''.join(map(str, signal))


def pattern(length, times) -> Signal:
    repeated = (repeat(n, times) for n in PATTERN)
    looped = cycle(chain.from_iterable(repeated))
    return tuple(islice(looped, 1, length + 1))


def apply_phase_of_fft(signal: Signal) -> int:
    n = len(signal)
    patterns = [pattern(n, i) for i in range(1, n + 1)]
    apply_pattern = lambda i: starmap(mul, zip(signal, patterns[i]))
    get_digit = lambda i: abs(sum(apply_pattern(i))) % 10
    return tuple(get_digit(i) for i in range(n))


def apply_n_phases(signal: Signal, n: int) -> Signal:
    for _ in range(n):
        signal = apply_phase_of_fft(signal)
    return signal[:8]


def real_signal(signal: Signal) -> Signal:
    input_signal = signal * 10_000
    offset = int(to_str(signal[:7]))
    result_signal = apply_n_phases(input_signal, 100)
    return result_signal[offset : offset + 8]


def solve() -> tuple[int, int]:
    signal = parse(read_puzzle())
    part1 = to_str(apply_n_phases(signal, 100))
    return part1, 0


if __name__ == '__main__':
    print(solve())