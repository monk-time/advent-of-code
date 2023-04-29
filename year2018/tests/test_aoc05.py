from ..aoc05 import are_matching, improve, react, solve

sample = 'dabAcCaCBAcCcaDA'


def test_are_matching():
    assert are_matching('a', 'A') is True
    assert are_matching('B', 'b') is True
    assert are_matching('C', 'C') is False
    assert are_matching('d', 'd') is False
    assert are_matching('e', 'f') is False
    assert are_matching('G', 'H') is False


def test_react():
    assert react('aA') == ''
    assert react('abBA') == ''
    assert react('abAB') == 'abAB'
    assert react('aabAAB') == 'aabAAB'
    assert react(sample) == 'dabCBAcaDA'


def test_react_with_skips():
    assert react(sample, 'a') == 'dbCBcD'
    assert react(sample, 'b') == 'daCAcaDA'
    assert react(sample, 'c') == 'daDA'
    assert react(sample, 'd') == 'abCBAc'


def test_improve():
    assert improve(sample) == 4


def test_solve():
    assert solve() == (9704, 6942)
