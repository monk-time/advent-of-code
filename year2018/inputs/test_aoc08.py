from aoc08 import metadata
from helpers import read_puzzle


def test_get_metadata():
    assert metadata('0 0') == []
    assert metadata('0 1 2') == [2]
    assert metadata('0 2 3 4') == [3, 4]
    puzzle = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    #         A----------------------------------
    #             B----------- C-----------
    #                              D-----
    assert metadata(puzzle) == [10, 11, 12, 99, 2, 1, 1, 2]
    puzzle = '2 3 1 1 0 1 99 2 0 3 10 11 12 1 1 2'
    #         A----------------------------------
    #             C----------- B-----------
    #                 D-----
    assert metadata(puzzle) == [99, 2, 10, 11, 12, 1, 1, 2]
    puzzle = '1 3 1 2 0 1 7 8 9 1 1 2'
    #         A----------------------
    #             C------------
    #                 D----
    assert metadata(puzzle) == [7, 8, 9, 1, 1, 2]
    puzzle = '1 3 1 2 1 1 0 1 6 7 8 9 1 1 2'
    #         A----------------------------
    #             C------------------
    #                 D----------
    #                     E----
    assert metadata(puzzle) == [6, 7, 8, 9, 1, 1, 2]


def test_full_puzzle():
    puzzle = read_puzzle()
    assert sum(metadata(puzzle)) == 35852
