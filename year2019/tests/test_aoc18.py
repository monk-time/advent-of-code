from inspect import cleandoc

import pytest

from year2019.aoc18 import (
    find_reachable_keys_bfs,
    parse,
    shortest_path_len,
    solve,
)

sample1 = cleandoc("""
    #########
    #b.A.@.a#
    #########
""")

sample2 = cleandoc("""
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
""")

sample3 = cleandoc("""
    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################
""")

sample4 = cleandoc("""
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

sample5 = cleandoc("""
    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################
""")


@pytest.mark.parametrize(
    'sample, start, result',
    (
        (sample1, (5, 1), [('a', 2, []), ('b', 4, ['a'])]),
        (sample1, (3, 1), [('a', 4, []), ('b', 2, [])]),
        (sample1, (1, 1), [('a', 6, ['a'])]),
        (sample2, (6, 1), [('e', 1, []), ('f', 5, ['e', 'd'])]),
        (
            sample4,
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
    ),
)
def test_find_reachable_keys_bfs(sample, start, result):
    tiles = parse(sample)
    assert sorted(find_reachable_keys_bfs(tiles, start)) == result


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample1, 8),
        (sample2, 86),
        (sample3, 132),
        (sample4, 136),
        (sample5, 81),
    ),
)
def test_shortest_path_len(sample, result):
    assert shortest_path_len(parse(sample)) == result


def test_solve():
    assert solve() == (4510, 0)
