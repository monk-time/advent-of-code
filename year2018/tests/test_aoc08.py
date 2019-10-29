import pytest

from aoc08 import Node, metadata_as_indices, metadata_rec, parse_tree, solve

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
def test_metadata_rec(input_str, tree_str, metadata):
    tree = parse_tree(input_str)
    assert list(metadata_rec(tree)) == metadata


def node_to_str(node: Node) -> str:
    meta_str = ' '.join(map(str, node.meta))
    children_str = ' '.join(map(node_to_str, node.children))
    if children_str:
        children_str += ' '
    return f'[{len(node.children)} {len(node.meta)} {children_str}({meta_str})]'


@pytest.mark.parametrize("input_str, tree_str, metadata", samples)
def test_build_tree(input_str, tree_str, metadata):
    assert node_to_str(parse_tree(input_str)) == tree_str


def test_metadata_as_indices():
    tree = parse_tree('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2')
    assert metadata_as_indices(tree) == 66


def test_solve():
    assert solve() == (35852, 33422)
