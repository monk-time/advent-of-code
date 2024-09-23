from inspect import cleandoc

from year2020.aoc06 import (
    count_questions_all,
    count_questions_any,
    parse,
    solve,
)

sample = cleandoc("""
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b
""")


def test_count_questions_any():
    assert count_questions_any(parse(sample)) == 11


def test_count_questions_all():
    assert count_questions_all(parse(sample)) == 6


def test_solve():
    assert solve() == (6530, 3323)
