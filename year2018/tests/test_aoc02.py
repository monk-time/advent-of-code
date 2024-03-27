import pytest

from year2018.aoc02 import (
    checksum,
    has_exactly_n_of_any_letter,
    is_correct_pair,
    matching_letters,
    part2,
    solve,
)

box_ids = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab',
]
bools2 = [False, True, True, False, True, True, False]
bools3 = [False, True, False, True, False, False, True]


@pytest.mark.parametrize('box_id, expected', zip(box_ids, bools2))
def test_has_exactly_n_of_any_letter_basic_2(box_id, expected):
    assert has_exactly_n_of_any_letter(box_id, 2) == expected


@pytest.mark.parametrize('box_id, expected', zip(box_ids, bools3))
def test_has_exactly_n_of_any_letter_basic_3(box_id, expected):
    assert has_exactly_n_of_any_letter(box_id, 3) == expected


def test_checksum():
    assert checksum(box_ids) == 12


def test_matching_letters():
    assert matching_letters('abcde', 'axcye') == 'ace'
    assert matching_letters('fghij', 'fguij') == 'fgij'


def test_is_correct_pair():
    assert not is_correct_pair('abcde', 'axcye')
    assert is_correct_pair('fghij', 'fguij')


def test_part2():
    box_ids2 = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
    assert part2(box_ids2) == 'fgij'


def test_solve():
    assert solve() == (5390, 'nvosmkcdtdbfhyxsphzgraljq')
