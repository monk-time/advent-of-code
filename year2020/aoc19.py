# https://adventofcode.com/2020/day/19

import re
from collections import deque
from itertools import chain

from utils_proxy import read_puzzle

# Patterns consist of two halves separated by |
# Each half is a sequence of either rule indices or literal characters
type Pattern = tuple[tuple[str | int, ...], ...]
type Rules = dict[int, Pattern]
type ResolvedRules = dict[int, str]


def soft_int(s: str) -> int | str:
    return int(s) if s.isdigit() else s


def parse(s: str) -> tuple[Rules, list[str]]:
    lines, msgs = [x.splitlines() for x in s.split('\n\n')]
    rules: Rules = {}
    for line in lines:
        idx, pattern = line.split(': ')
        idx = int(idx)
        pattern = pattern.replace('"', '')
        halves = pattern.split(' | ')
        rules[idx] = tuple(
            tuple(map(soft_int, half.split())) for half in halves
        )
    return rules, msgs


def resolve(rules: Rules) -> ResolvedRules:
    queue = deque([0])
    resolved: ResolvedRules = {}
    while queue:
        idx = queue.popleft()
        if idx in resolved:
            continue
        cur_len = len(queue)
        for x in chain.from_iterable(rules[idx]):
            if isinstance(x, int) and x not in resolved:
                queue.append(x)
        if len(queue) != cur_len:
            queue.append(idx)
            continue
        resolved[idx] = '|'.join(
            ''.join(resolved[x] if isinstance(x, int) else x for x in half)
            for half in rules[idx]
        )
        if len(rules[idx]) == 2:
            resolved[idx] = f'({resolved[idx]})'
    return resolved


def count_part1(resolved: ResolvedRules, msgs: list[str]) -> int:
    return sum(1 for msg in msgs if re.fullmatch(resolved[0], msg))


def count_part2(resolved: ResolvedRules, msgs: list[str]) -> int:
    # Rule 0 is always 42 42 31.
    # With changes for part 2 it becomes 42+ 42{n} 31{n},
    # or 42+ 31+ where 42 appears more times than 31.
    re_x, re_y = resolved[42], resolved[31]
    pattern = f'(?P<x>({re_x})+)(?P<y>({re_y})+)'
    return sum(
        1
        for msg in msgs
        if (m := re.fullmatch(pattern, msg))
        and len(re.findall(re_x, m.group('x')))
        > len(re.findall(re_y, m.group('y')))
    )


def solve() -> tuple[int, int]:
    rules, msgs = parse(read_puzzle())
    resolved = resolve(rules)
    return (count_part1(resolved, msgs), count_part2(resolved, msgs))


if __name__ == '__main__':
    print(solve())
