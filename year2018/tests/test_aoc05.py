from aoc05 import are_matching, react, improve
from helpers import read_puzzle


def test_are_matching():
    assert are_matching('a', 'A') is True
    assert are_matching('B', 'b') is True
    assert are_matching('C', 'C') is False
    assert are_matching('d', 'd') is False
    assert are_matching('e', 'f') is False
    assert are_matching('G', 'H') is False


def test_react():
    assert ''.join(react('aA')) == ''
    assert ''.join(react('abBA')) == ''
    assert ''.join(react('abAB')) == 'abAB'
    assert ''.join(react('aabAAB')) == 'aabAAB'
    assert ''.join(react('dabAcCaCBAcCcaDA')) == 'dabCBAcaDA'


def test_improve():
    assert improve('dabAcCaCBAcCcaDA') == 4


def test_full_puzzle():
    puzzle = read_puzzle()
    assert len(react(puzzle)) == 9704
    assert improve(puzzle) == 6942
