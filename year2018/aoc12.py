# https://adventofcode.com/2018/day/12

import re
from collections import deque
from itertools import islice
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

sample = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

State = tuple[str, int]  # a row of pots and an index of the pot #0


def parse(input_str: str) -> tuple[set[str], State]:
    (pots, _), *rules = re.findall(r'([#.]+)(?: => ([#.]))?', input_str)
    return {seq for seq, res in rules if res == '#'}, pad(pots, 0)


def pad(pots: str, i_zero: int) -> State:
    """Ensure that pots start with '....#' and end with '#....'."""
    pots = pots.rstrip('.') + '....'
    extra = pots.index('#') - 4
    if extra > 0:
        return pots[extra:], i_zero - extra
    if extra < 0:
        return '.' * (-extra) + pots, i_zero - extra
    return pots, i_zero


def next_gen(rules: set[str], pots: str, i_zero: int) -> State:
    """Get the next generation. Pots must be already padded."""
    pots = '..' + ''.join(
        '#' if pots[i - 2 : i + 3] in rules else '.'
        for i in range(2, len(pots) - 2)
    )
    return pad(pots, i_zero)


def evolve(rules: set[str], pots: str, i_zero: int) -> Iterable[State]:
    while True:
        yield pots, i_zero
        pots, i_zero = next_gen(rules, pots, i_zero)


def str_n_gens(gens: int, rules: set[str], pots: str, i_zero: int):
    states = list(
        islice(evolve(rules, pots, i_zero), gens + 1)
    )  # including gen. #0
    max_i_zero = max(i_zero for _, i_zero in states)
    lines = [(max_i_zero - i_zero) * '.' + pots for pots, i_zero in states]
    max_len = max(len(pots) for pots in lines)
    return [
        f'{i:{len(str(gens))}d}: {pots.ljust(max_len, ".")}'
        for i, pots in enumerate(lines)
    ]


def sum_of_pots(pots: str, i_zero: int) -> int:
    return sum(i - i_zero for i, p in enumerate(pots) if p == '#')


def sum_of_pots_at_gen(
    gen: int, rules: set[str], pots: str, i_zero: int
) -> int:
    gen_n = next(islice(evolve(rules, pots, i_zero), gen, None))
    return sum_of_pots(*gen_n)


def stabilize(rules: set[str], pots: str, i_zero: int) -> tuple[int, int, int]:
    prev_sum = sum_of_pots(pots, i_zero)
    deltas = deque([0, prev_sum], maxlen=5)
    gen = 0
    while len(set(deltas)) > 1:
        gen += 1
        pots, i_zero = next_gen(rules, pots, i_zero)
        next_sum = sum_of_pots(pots, i_zero)
        deltas.append(next_sum - prev_sum)
        prev_sum = next_sum
    return gen, prev_sum, deltas[0]


def solve():
    rules, state = parse(read_puzzle())
    gen, sum_, delta = stabilize(rules, *state)
    return (
        sum_of_pots_at_gen(20, rules, *state),
        sum_ + (50000000000 - gen) * delta,
    )


if __name__ == '__main__':
    print(solve())
