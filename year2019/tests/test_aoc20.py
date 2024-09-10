from inspect import cleandoc

import pytest

from year2019.aoc20 import TileMap, find_min_path_len, solve


def preserve_whitespace(s: str) -> str:
    """Avoid problems with linters and autoformatting on save."""
    return cleandoc(s).replace('|', '')


sample1 = preserve_whitespace("""
    |   A    |
    |   A    |
    |  #.##  |
    |BB..##  |
    |  ####  |
    |BB....ZZ|
    |  ####  |
""")

sample2 = preserve_whitespace("""
    |         A           |
    |         A           |
    |  #######.#########  |
    |  #######.........#  |
    |  #######.#######.#  |
    |  #######.#######.#  |
    |  #######.#######.#  |
    |  #####  B    ###.#  |
    |BC...##  C    ###.#  |
    |  ##.##       ###.#  |
    |  ##...DE  F  ###.#  |
    |  #####    G  ###.#  |
    |  #########.#####.#  |
    |DE..#######...###.#  |
    |  #.#########.###.#  |
    |FG..#########.....#  |
    |  ###########.#####  |
    |             Z       |
    |             Z       |
""")

sample3 = preserve_whitespace("""
    |                   A               |
    |                   A               |
    |  #################.#############  |
    |  #.#...#...................#.#.#  |
    |  #.#.#.###.###.###.#########.#.#  |
    |  #.#.#.......#...#.....#.#.#...#  |
    |  #.#########.###.#####.#.#.###.#  |
    |  #.............#.#.....#.......#  |
    |  ###.###########.###.#####.#.#.#  |
    |  #.....#        A   C    #.#.#.#  |
    |  #######        S   P    #####.#  |
    |  #.#...#                 #......VT|
    |  #.#.#.#                 #.#####  |
    |  #...#.#               YN....#.#  |
    |  #.###.#                 #####.#  |
    |DI....#.#                 #.....#  |
    |  #####.#                 #.###.#  |
    |ZZ......#               QG....#..AS|
    |  ###.###                 #######  |
    |JO..#.#.#                 #.....#  |
    |  #.#.#.#                 ###.#.#  |
    |  #...#..DI             BU....#..LF|
    |  #####.#                 #.#####  |
    |YN......#               VT..#....QG|
    |  #.###.#                 #.###.#  |
    |  #.#...#                 #.....#  |
    |  ###.###    J L     J    #.#.###  |
    |  #.....#    O F     P    #.#...#  |
    |  #.###.#####.#.#####.#####.###.#  |
    |  #...#.#.#...#.....#.....#.#...#  |
    |  #.#####.###.###.#.#.#########.#  |
    |  #...#.#.....#...#.#.#.#.....#.#  |
    |  #.###.#####.###.###.#.#.#######  |
    |  #.#.........#...#.............#  |
    |  #########.###.###.#############  |
    |           B   J   C               |
    |           U   P   P               |
""")


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample1, 6),
        (sample2, 23),
        (sample3, 58),
    ),
)
def test_find_min_path_len(sample, result):
    assert find_min_path_len(TileMap.from_str(sample)) == result


def test_solve():
    assert solve() == (496, 0)
