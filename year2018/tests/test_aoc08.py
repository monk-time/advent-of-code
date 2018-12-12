import pytest

from aoc08 import build_tree, metadata_as_indices, metadata_linear, metadata_rec, parse
from helpers import read_puzzle

samples = [
    ('0 0', '[0 0 ()]', []),
    ('0 1 2', '[0 1 (2)]', [2]),
    ('0 2 3 4', '[0 2 (3 4)]', [3, 4]),
    ('1 2 0 1 12 10 11', '[1 2 [0 1 (12)] (10 11)]', [12, 10, 11]),
    (
        #  2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
        #  A----------------------------------
        #      B----------- C-----------
        #                       D-----
        '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2',
        '[2 3 [0 3 (10 11 12)] [1 1 [0 1 (99)] (2)] (1 1 2)]',
        [10, 11, 12, 99, 2, 1, 1, 2],
    ),
    (
        # 2 3 1 1 0 1 99 2 0 3 10 11 12 1 1 2
        # A----------------------------------
        #     B----------- D-----------
        #         C-----
        '2 3 1 1 0 1 99 2 0 3 10 11 12 1 1 2',
        '[2 3 [1 1 [0 1 (99)] (2)] [0 3 (10 11 12)] (1 1 2)]',
        [99, 2, 10, 11, 12, 1, 1, 2],
    ),
    (
        # 1 3 1 2 0 1 7 8 9 1 1 2
        # A----------------------
        #     B------------
        #         C----
        '1 3 1 2 0 1 7 8 9 1 1 2',
        '[1 3 [1 2 [0 1 (7)] (8 9)] (1 1 2)]',
        [7, 8, 9, 1, 1, 2],
    ),
    (
        # 1 3 1 2 1 1 0 1 6 7 8 9 1 1 2
        # A----------------------------
        #     B------------------
        #         C----------
        #             D----
        '1 3 1 2 1 1 0 1 6 7 8 9 1 1 2',
        '[1 3 [1 2 [1 1 [0 1 (6)] (7)] (8 9)] (1 1 2)]',
        [6, 7, 8, 9, 1, 1, 2],
    ),

]


@pytest.mark.parametrize("input_str, tree_str, metadata", samples)
def test_metadata(input_str, tree_str, metadata):
    assert metadata_linear(parse(input_str)) == metadata


@pytest.mark.parametrize("input_str, tree_str, metadata", samples)
def test_build_tree(input_str, tree_str, metadata):
    assert str(build_tree(parse(input_str))) == tree_str


def test_metadata_as_indices():
    tree = build_tree(parse('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'))
    assert metadata_as_indices(tree) == 66


def test_full_puzzle():
    puzzle = parse(read_puzzle())
    assert sum(metadata_linear(puzzle)) == 35852

    tree = build_tree(puzzle)
    assert sum(metadata_rec(tree)) == 35852
    assert metadata_as_indices(tree) == 33422
