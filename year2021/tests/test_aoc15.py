from inspect import cleandoc

from year2021.aoc15 import expand, find_min_path, parse, solve

sample = cleandoc("""
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
""")


def test_find_min_path():
    assert find_min_path(parse(sample)) == 40


def test_find_min_path_large():
    assert find_min_path(expand(parse(sample))) == 315


def test_solve():
    assert solve() == (553, 2858)
