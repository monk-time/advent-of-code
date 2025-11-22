# https://adventofcode.com/2020/day/7

from collections import Counter

from utils_proxy import read_puzzle

type Bag = Counter[str]
type Bags = dict[str, Bag]


def parse_bag(line: str) -> tuple[str, Bag]:
    name, content = line.split(' bags contain ')
    content = content.rstrip('.').replace(' bags', '').replace(' bag', '')
    if content == 'no other':
        return name, Counter()
    bags = [s.split(' ', 1) for s in content.split(', ')]
    return name, Counter({bag[1]: int(bag[0]) for bag in bags})


def parse(s: str) -> Bags:
    return dict(parse_bag(line) for line in s.split('\n'))


def mul[T](counter: Counter[T], n: int) -> Counter[T]:
    return Counter({k: n * v for k, v in counter.items()})


def resolve(bags: Bags) -> Bags:
    stack = [*bags]
    resolved: Bags = {}
    while stack:
        bag = stack.pop()
        if bag in resolved:
            continue
        unresolved_parts = bags[bag] - resolved.keys()
        if unresolved_parts:
            stack.extend((bag, *unresolved_parts))
            continue
        resolved[bag] = sum(
            (mul(resolved[in_bag], n) for in_bag, n in bags[bag].items()),
            start=bags[bag],
        )
    return resolved


def solve() -> tuple[int, int]:
    resolved_bags = resolve(parse(read_puzzle()))
    return (
        sum('shiny gold' in c for c in resolved_bags.values()),
        sum(resolved_bags['shiny gold'].values()),
    )


if __name__ == '__main__':
    print(solve())
