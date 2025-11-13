from itertools import islice

import pytest

from year2020.aoc15 import PART_1, PART_2, gen_memory_game, get_nth_num, solve


def test_gen_memory_game():
    first_10 = tuple(islice(gen_memory_game((0, 3, 6)), 10))
    assert first_10 == (0, 3, 6, 0, 3, 3, 1, 0, 4, 0)


@pytest.mark.parametrize(
    'start_nums, result',
    (
        ((0, 3, 6), 436),
        ((1, 3, 2), 1),
        ((2, 1, 3), 10),
        ((1, 2, 3), 27),
        ((2, 3, 1), 78),
        ((3, 2, 1), 438),
        ((3, 1, 2), 1836),
    ),
)
def test_get_2020th_num(start_nums: tuple[int, ...], result: int):
    assert get_nth_num(start_nums, PART_1) == result


@pytest.mark.parametrize(
    'start_nums, result',
    (
        ((0, 3, 6), 175594),
        ((1, 3, 2), 2578),
        ((2, 1, 3), 3544142),
        ((1, 2, 3), 261214),
        ((2, 3, 1), 6895259),
        ((3, 2, 1), 18),
        ((3, 1, 2), 362),
    ),
)
def test_get_30000000th_num(start_nums: tuple[int, ...], result: int):
    assert get_nth_num(start_nums, PART_2) == result


def test_solve():
    assert solve() == (700, 51358)
