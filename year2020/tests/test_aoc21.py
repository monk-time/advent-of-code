from inspect import cleandoc

import pytest

from year2020.aoc21 import (
    AlrgMap,
    Food,
    count_safe,
    find_allergens,
    format_bad_ingrs,
    parse,
    solve,
)

sample = cleandoc("""
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)
""")


@pytest.fixture(scope='module')
def foods() -> list[Food]:
    return list(parse(sample))


@pytest.fixture(scope='module')
def alrg_map(foods: list[Food]) -> AlrgMap:
    return find_allergens(foods)


def test_find_allergens(foods: list[Food]):
    assert find_allergens(foods) == {
        'fish': 'sqjhc',
        'dairy': 'mxmxvkd',
        'soy': 'fvjkl',
    }


def test_count_safe(foods: list[Food], alrg_map: AlrgMap):
    assert count_safe(foods, alrg_map) == 5


def test_format_bad_ingrs(alrg_map: AlrgMap):
    assert format_bad_ingrs(alrg_map) == 'mxmxvkd,sqjhc,fvjkl'


def test_solve():
    assert solve() == (2078, 'lmcqt,kcddk,npxrdnd,cfb,ldkt,fqpt,jtfmtpd,tsch')
