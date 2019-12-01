def decoded():
    # Manually reconstructed from the input
    d = 0
    while True:
        c = d | 65536
        d = 1397714
        while True:
            d = (((d + (c & 255)) & 16777215) * 65899) & 16777215
            if c < 256:
                break
            c //= 256
        yield d


def solve():
    gen = decoded()
    exit_values = []
    while True:
        reg_a = next(gen)
        if reg_a in exit_values:
            break
        exit_values.append(reg_a)

    return exit_values[0], exit_values[-1]


if __name__ == '__main__':
    print(solve())
