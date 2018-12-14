import re
from itertools import islice
from typing import Iterable, Set, Tuple

from helpers import read_puzzle

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

State = Tuple[str, int]  # a row of pots and an index of the pot #0


def parse(input_str: str) -> Tuple[Set[str], State]:
    (pots, _), *rules = re.findall(r'([#.]+)(?: => ([#.]))?', input_str)
    return set(seq for seq, res in rules if res == '#'), pad(pots, 0)


def pad(pots: str, i_zero: int) -> State:
    """Ensure that pots start with '....#' and end with '#....'."""
    pots = pots.rstrip('.') + '....'
    extra = pots.index('#') - 4
    if extra > 0:
        return pots[extra:], i_zero - extra
    if extra < 0:
        return '.' * (-extra) + pots, i_zero - extra
    return pots, i_zero


def next_gen(rules: Set[str], pots: str, i_zero: int = 4) -> State:
    """Get the next generation. Pots must be already padded."""
    pots = '..' + ''.join('#' if pots[i - 2:i + 3] in rules else '.'
                          for i in range(2, len(pots) - 2))
    return pad(pots, i_zero)


def evolve(rules: Set[str], pots: str, i_zero: int = 4) -> Iterable[State]:
    while True:
        yield pots, i_zero
        pots, i_zero = next_gen(rules, pots, i_zero)


def sum_of_pots(pots: str, i_zero: int) -> int:
    return sum(i - i_zero for i, p in enumerate(pots) if p == '#')


if __name__ == '__main__':
    rules_, state = parse(read_puzzle())
    gen20 = next(islice(evolve(rules_, *state), 20, None))
    print(sum_of_pots(*gen20))
