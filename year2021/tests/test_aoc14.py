from collections import Counter
from inspect import cleandoc

import pytest

from year2021.aoc14 import Pairs, Rules, merge, next_step, parse, score, solve

sample = cleandoc("""
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
""")


@pytest.fixture(scope='module')
def sample_obj() -> tuple[Pairs, Rules]:
    return parse(sample)


def test_next_step(sample_obj: tuple[Pairs, Rules]):
    poly, rules = sample_obj
    poly = next_step(poly, rules)
    assert merge(poly) == Counter('NCNBCHB')
    poly = next_step(poly, rules)
    assert merge(poly) == Counter('NBCCNBBBCBHCB')
    poly = next_step(poly, rules)
    assert merge(poly) == Counter('NBBBCNCCNBBNBNBBCHBHHBCHB')
    poly = next_step(poly, rules)
    assert merge(poly) == Counter(
        'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    )


@pytest.mark.parametrize(
    'steps, result',
    (
        (10, 1588),
        (40, 2188189693529),
    ),
)
def test_score(steps: int, result: int, sample_obj: tuple[Pairs, Rules]):
    assert score(*sample_obj, steps) == result


def test_solve():
    assert solve() == (2899, 3528317079545)
