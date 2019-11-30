def run(a: int):
    # Manually reconstructed from the input
    b = (1010, 10551410)[a]
    return sum(d for d in range(1, b + 1) if b % d == 0)


def solve():
    return run(0), run(1)


if __name__ == '__main__':
    print(solve())
