from inspect import cleandoc

import pytest

from year2019.aoc22 import shuffle, solve, view

sample1 = cleandoc("""
    deal with increment 7
    deal into new stack
    deal into new stack
""")

sample2 = cleandoc("""
    cut 6
    deal with increment 7
    deal into new stack
""")

sample3 = cleandoc("""
    deal with increment 7
    deal with increment 9
    cut -2
""")

sample4 = cleandoc("""
    deal into new stack
    cut -2
    deal with increment 7
    cut 8
    cut -4
    deal with increment 7
    cut 3
    deal with increment 9
    deal with increment 3
    cut -1
""")


@pytest.mark.parametrize(
    'sample, result',
    (
        ('deal into new stack', (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)),
        ('cut 3', (3, 4, 5, 6, 7, 8, 9, 0, 1, 2)),
        ('cut -4', (6, 7, 8, 9, 0, 1, 2, 3, 4, 5)),
        ('deal with increment 3', (0, 7, 4, 1, 8, 5, 2, 9, 6, 3)),
        ('deal with increment 9', (0, 9, 8, 7, 6, 5, 4, 3, 2, 1)),
        (sample1, (0, 3, 6, 9, 2, 5, 8, 1, 4, 7)),
        (sample2, (3, 0, 7, 4, 1, 8, 5, 2, 9, 6)),
        (sample3, (6, 3, 0, 7, 4, 1, 8, 5, 2, 9)),
        (sample4, (9, 2, 5, 8, 1, 4, 7, 0, 3, 6)),
    ),
)
def test_shuffle(sample, result):
    start, step = shuffle(sample.splitlines(), 10)
    assert view(start, step, 10) == result


def test_solve():
    assert solve() == (4649, 68849657493596)
