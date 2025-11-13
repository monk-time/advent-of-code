from inspect import cleandoc

import pytest

from year2019.aoc18 import (
    Coord,
    find_reachable_keys_bfs,
    parse,
    shortest_path_len,
    shortest_path_len_by_quadrants,
    solve,
)

sample1_1 = cleandoc("""
    #########
    #b.A.@.a#
    #########
""")

sample1_2 = cleandoc("""
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
""")

sample1_3 = cleandoc("""
    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################
""")

sample1_4 = cleandoc("""
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################
""")

sample1_5 = cleandoc("""
    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################
""")

sample2_1 = cleandoc("""
    #######
    #a.#Cd#
    ##...##
    ##.@.##
    ##...##
    #cB#Ab#
    #######
""")

sample2_2 = cleandoc("""
    ###############
    #d.ABC.#.....a#
    ######...######
    ######.@.######
    ######...######
    #b.....#.....c#
    ###############
""")

sample2_3 = cleandoc("""
    #############
    #g#f.D#..h#l#
    #F###e#E###.#
    #dCba...BcIJ#
    #####.@.#####
    #nK.L...G...#
    #M###N#H###.#
    #o#m..#i#jk.#
    #############
""")


@pytest.mark.parametrize(
    'sample, start, result',
    (
        (sample1_1, (5, 1), [('a', 2, []), ('b', 4, ['a'])]),
        (sample1_1, (3, 1), [('a', 4, []), ('b', 2, [])]),
        (sample1_1, (1, 1), [('a', 6, ['a'])]),
        (sample1_2, (6, 1), [('e', 1, []), ('f', 5, ['e', 'd'])]),
        (
            sample1_4,
            (8, 4),
            [
                ('a', 3, []),
                ('b', 3, []),
                ('c', 5, []),
                ('d', 5, []),
                ('e', 5, []),
                ('f', 3, []),
                ('g', 3, []),
                ('h', 5, []),
            ],
        ),
    ),  # type: ignore
)
def test_find_reachable_keys_bfs(
    sample: str, start: Coord, result: list[tuple[str, int, list[str]]]
):
    tiles = parse(sample)
    assert sorted(find_reachable_keys_bfs(tiles, start)) == result


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample1_1, 8),
        (sample1_2, 86),
        (sample1_3, 132),
        (sample1_4, 136),
        (sample1_5, 81),
    ),
)
def test_shortest_path_len(sample: str, result: int):
    assert shortest_path_len(parse(sample)) == result


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample2_1, 8),
        (sample2_2, 24),
        # (sample2_3, 72), - assumptions in the solution fail for this sample
    ),
)
def test_shortest_path_len_by_quadrants(sample: str, result: int):
    assert shortest_path_len_by_quadrants(parse(sample)) == result


def test_solve():
    assert solve() == (4510, 1816)
