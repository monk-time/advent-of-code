from year2021.aoc17 import gen_max_heights, parse, solve

sample = 'target area: x=20..30, y=-10..-5'


def test_gen_max_heights():
    max_heights = list(gen_max_heights(parse(sample)))
    assert max(max_heights) == 45
    assert len(max_heights) == 112


def test_solve():
    assert solve() == (10878, 4716)
