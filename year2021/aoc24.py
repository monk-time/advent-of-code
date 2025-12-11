# https://adventofcode.com/2021/day/24
# tags: #instructions #virtual-machine #reverse-engineering

from itertools import product, starmap

type Program = tuple[tuple[str, ...], ...]


def parse(s: str) -> Program:
    return tuple(tuple(line.split()) for line in s.splitlines())


def execute(program: Program, input_vals: tuple[int, ...]) -> int:
    def get_value(x: str) -> int:
        return int(x) if x.lstrip('-').isdigit() else mem[ord(x) - ord('w')]

    mem = [0, 0, 0, 0]
    input_idx = 0
    for line in program:
        command = (line[0], ord(line[1]) - ord('w'), *line[2:])
        match command:
            case ('inp', x):
                mem[x] = input_vals[input_idx]
                input_idx += 1
            case ('add', x, y):
                mem[x] += get_value(y)
            case ('mul', x, y):
                mem[x] *= get_value(y)
            case ('div', x, y):
                mem[x] //= get_value(y)
            case ('mod', x, y):
                mem[x] %= get_value(y)
            case ('eql', x, y):
                mem[x] = int(mem[x] == get_value(y))
            case _:
                raise ValueError(command)
    return mem[3]


def execute_decoded(input_vals: tuple[int, ...]) -> int:
    # Manually decoded from the input
    z = 0
    a = input_vals
    z = z * 26 + a[0] + 8
    z = z * 26 + a[1] + 8
    z = z * 26 + a[2] + 3
    z = z * 26 + a[3] + 10
    z = z - z % 26 + a[4] + 8 if z % 26 != a[4] + 12 else z // 26
    z = z * 26 + a[5] + 8
    z = z - z % 26 + a[6] + 8 if z % 26 != a[6] + 2 else z // 26
    z = z - z % 26 + a[7] + 5 if z % 26 != a[7] + 11 else z // 26
    z = z * 26 + a[8] + 9
    z = z * 26 + a[9] + 3
    z = z - z % 26 + a[10] + 4 if z % 26 != a[10] else z // 26
    z = z - z % 26 + a[11] + 9 if z % 26 != a[11] + 12 else z // 26
    z = z - z % 26 + a[12] + 2 if z % 26 != a[12] + 13 else z // 26
    z = z - z % 26 + a[13] + 7 if z % 26 != a[13] + 6 else z // 26
    return z  # noqa: RET504


def is_valid(a: tuple[int, ...]) -> bool:
    return (
        a[3] == a[4] + 2
        and a[5] + 6 == a[6]
        and a[2] == a[7] + 8
        and a[9] + 3 == a[10]
        and a[8] == a[11] + 3
        and a[1] == a[12] + 5
        and a[0] + 2 == a[13]
    )


def to_valid(*args: int) -> int | None:
    a, b, c, d, e, f, g = args
    r = [a, b, c, d, d - 2, e, e + 6, c - 8, f, g, g + 3, f - 3, b - 5, a + 2]
    if not all(1 <= x <= 9 for x in r):
        return None
    return int(''.join(str(x) for x in r))


def solve() -> tuple[int, int]:
    def first_valid(r: range) -> int:
        return next(filter(None, starmap(to_valid, product(r, repeat=7))))

    return first_valid(range(9, 0, -1)), first_valid(range(1, 10))


if __name__ == '__main__':
    print(solve())
