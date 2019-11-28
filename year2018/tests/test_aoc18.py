from inspect import cleandoc

import pytest

from aoc18 import Map, count_after_n_ticks, solve

sample_str = cleandoc("""
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..|.
    ...#.|..|.
""")


@pytest.fixture
def sample():
    return Map(sample_str)


def test_map_init(sample):
    assert sample.height == sample.width == 10
    assert sample.m[(0, 0)] == '.'
    assert sample.m[(0, 1)] == '#'


def test_map_str(sample):
    assert str(sample) == sample_str


def test_map_tick(sample):
    sample.tick()
    assert str(sample) == cleandoc("""
        .......##.
        ......|###
        .|..|...#.
        ..|#||...#
        ..##||.|#|
        ...#||||..
        ||...|||..
        |||||.||.|
        ||||||||||
        ....||..|.
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        .......#..
        ......|#..
        .|.|||....
        ..##|||..#
        ..###|||#|
        ...#|||||.
        |||||||||.
        ||||||||||
        ||||||||||
        .|||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        .......#..
        ....|||#..
        .|.||||...
        ..###|||.#
        ...##|||#|
        .||##|||||
        ||||||||||
        ||||||||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        .....|.#..
        ...||||#..
        .|.#||||..
        ..###||||#
        ...###||#|
        |||##|||||
        ||||||||||
        ||||||||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        ....|||#..
        ...||||#..
        .|.##||||.
        ..####|||#
        .|.###||#|
        |||###||||
        ||||||||||
        ||||||||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        ...||||#..
        ...||||#..
        .|.###|||.
        ..#.##|||#
        |||#.##|#|
        |||###||||
        ||||#|||||
        ||||||||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        ...||||#..
        ..||#|##..
        .|.####||.
        ||#..##||#
        ||##.##|#|
        |||####|||
        |||###||||
        ||||||||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        ..||||##..
        ..|#####..
        |||#####|.
        ||#...##|#
        ||##..###|
        ||##.###||
        |||####|||
        ||||#|||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        ..||###...
        .||#####..
        ||##...##.
        ||#....###
        |##....##|
        ||##..###|
        ||######||
        |||###||||
        ||||||||||
        ||||||||||
    """)

    sample.tick()
    assert str(sample) == cleandoc("""
        .||##.....
        ||###.....
        ||##......
        |##.....##
        |##.....##
        |##....##|
        ||##.####|
        ||#####|||
        ||||#|||||
        ||||||||||
    """)


def test_count_after_n_ticks(sample):
    assert count_after_n_ticks(sample, 10) == 1147


def test_solve():
    assert solve() == (549936, 206304)
