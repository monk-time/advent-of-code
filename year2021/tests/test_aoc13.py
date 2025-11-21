from inspect import cleandoc

from year2021.aoc13 import fold, fold_all, parse, solve

sample = cleandoc("""
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5
""")


def test_fold():
    grid, folds = parse(sample)
    assert len(fold(grid, folds[0])) == 17


def test_fold_all():
    grid, folds = parse(sample)
    assert len(fold_all(grid, folds)) == 16


def test_solve():
    assert solve() == (729, 100)
