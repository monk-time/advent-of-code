from inspect import cleandoc

from year2019.aoc18 import parse, shortest_path_len, solve

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


def test_shortest_path_len():
    assert shortest_path_len(parse(sample1)) == 8
    assert shortest_path_len(parse(sample2)) == 86
    assert shortest_path_len(parse(sample3)) == 132
    # assert shortest_path_len(parse(sample4)) == 136
    assert shortest_path_len(parse(sample5)) == 81


def test_solve():
    assert solve() == (0, 0)
