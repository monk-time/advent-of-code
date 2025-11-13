from inspect import cleandoc

import pytest

from year2018.aoc17 import Map, Point, add_water, count_wet, solve


@pytest.fixture
def sample() -> Map:
    return Map(
        cleandoc("""
            x=495, y=2..7
            y=7, x=495..501
            x=501, y=3..7
            x=498, y=2..4
            x=506, y=1..2
            x=498, y=10..13
            x=504, y=10..13
            y=13, x=498..504
        """)
    )


def test_map_init(sample: Map):
    assert sample.max_y == 13
    assert sample[Point(1, 506)] == '#'
    assert sample[Point(2, 506)] == '#'


def test_map_str(sample: Map):
    assert str(sample) == cleandoc("""
        ...........#
        #..#.......#
        #..#..#.....
        #..#..#.....
        #.....#.....
        #.....#.....
        #######.....
        ............
        ............
        ...#.....#..
        ...#.....#..
        ...#.....#..
        ...#######..
    """)


def test_add_water(sample: Map):
    add_water(sample)
    print()
    print(sample)
    assert str(sample) == cleandoc("""
        .....|.....#
        #..#||||...#
        #..#~~#|....
        #..#~~#|....
        #~~~~~#|....
        #~~~~~#|....
        #######|....
        .......|....
        ..|||||||||.
        ..|#~~~~~#|.
        ..|#~~~~~#|.
        ..|#~~~~~#|.
        ..|#######|.
    """)


def test_add_water_two_spills():
    m = Map(
        cleandoc("""
            x=499, y=2..3
            x=501, y=2..3
            y=3, x=499..501
            x=498, y=5..5
            x=495, y=8..10
            x=507, y=8..10
            y=10, x=495..507
        """)
    )
    add_water(m)
    assert str(m) == cleandoc("""
        ....|#~#|......
        ....|###|......
        ...|||..|......
        ...|#|..|......
        ...|.|..|......
        |||||||||||||||
        |#~~~~~~~~~~~#|
        |#~~~~~~~~~~~#|
        |#############|
    """)


def test_count_wet(sample: Map):
    assert count_wet(sample) == (0, 0)
    add_water(sample)
    assert count_wet(sample) == (57, 29)


def test_solve():
    assert solve() == (28246, 23107)
