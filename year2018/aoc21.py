# https://adventofcode.com/2018/day/21


def decoded():
    # Manually reconstructed from the input
    d = 0
    while True:
        c = d | 0x10000
        d = 1397714
        while c:
            d += c & 0xFF
            d &= 0xFFFFFF
            d *= 65899
            d &= 0xFFFFFF
            c >>= 8
        yield d


def solve():
    gen = decoded()
    exit_values: list[int] = []
    while True:
        reg_a = next(gen)
        if reg_a in exit_values:
            break
        exit_values.append(reg_a)

    return exit_values[0], exit_values[-1]


if __name__ == '__main__':
    print(solve())
