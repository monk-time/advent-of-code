import pytest

from year2020.aoc18 import calc_1, calc_2, parse_tokens, solve


@pytest.mark.parametrize(
    's, result',
    (
        ('1 + 2 * 3 + 4 * 5 + 6', 71),
        ('1 + (2 * 3) + (4 * (5 + 6))', 51),
        ('2 * 3 + (4 * 5)', 26),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
        ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
        ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632),
    ),
)
def test_calc_1(s, result):
    assert calc_1(parse_tokens(s)) == result


@pytest.mark.parametrize(
    's, result',
    (
        ('1 + 2 * 3 + 4 * 5 + 6', 231),
        ('1 + (2 * 3) + (4 * (5 + 6))', 51),
        ('2 * 3 + (4 * 5)', 46),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
        ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
        ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340),
    ),
)
def test_calc_2(s, result):
    assert calc_2(parse_tokens(s)) == result


def test_solve():
    assert solve() == (11076907812171, 283729053022731)
