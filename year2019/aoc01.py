from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def fuel(mass: int) -> int:
    return mass // 3 - 2


def fuel_req(mass: int) -> int:
    total = 0
    while True:
        mass = fuel(mass)
        if mass <= 0:
            break
        total += mass
    return total


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    part1 = sum(fuel(mass) for mass in puzzle)
    part2 = sum(fuel_req(mass) for mass in puzzle)
    return part1, part2


if __name__ == '__main__':
    print(solve())
