from aoc14 import improve, recipes_to_the_left
from helpers import read_puzzle


def test_improve():
    assert improve(9) == '5158916779'
    assert improve(5) == '0124515891'
    assert improve(18) == '9251071085'
    assert improve(2018) == '5941429882'


def test_recipes_to_the_left():
    assert recipes_to_the_left('51589') == 9
    assert recipes_to_the_left('01245') == 5
    assert recipes_to_the_left('92510') == 18
    assert recipes_to_the_left('59414') == 2018
    assert recipes_to_the_left('1589167') == 10


def test_full_puzzle():
    puzzle = read_puzzle()
    assert improve(int(puzzle)) == '9276422810'
    assert recipes_to_the_left(puzzle) == 20319117
