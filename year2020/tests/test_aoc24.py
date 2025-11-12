from inspect import cleandoc

from year2020.aoc24 import around, cycle, parse, solve

sample = cleandoc("""
    sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew
""")


def test_around():
    assert around((1, 1)) == ((2, 1), (1, 2), (0, 2), (0, 1), (1, 0), (2, 0))


def test_parse():
    assert len(parse(sample)) == 10


def test_cycle():
    tiles = parse(sample)
    for n in (15, 12, 25, 14, 23, 28, 41, 37, 49, 37):
        tiles = cycle(tiles)
        assert len(tiles) == n


def test_solve():
    assert solve() == (411, 4092)
