from inspect import cleandoc

import pytest

from year2018.aoc18 import Map, count_after_n_ticks, solve, update

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
def sample() -> Map:
    return Map.fromstring(sample_str)


def test_map_fromstring(sample: Map):
    assert sample.height == sample.width == 10
    assert sample.m[0][0] == '.'
    assert sample.m[0][1] == '#'


def test_map_str(sample: Map):
    assert str(sample) == sample_str


def test_update(sample: Map):
    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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

    sample = update(sample)
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


def test_count_after_n_ticks(sample: Map):
    assert count_after_n_ticks(sample, 10) == 1147


def test_solve():
    assert solve() == (549936, 206304)
