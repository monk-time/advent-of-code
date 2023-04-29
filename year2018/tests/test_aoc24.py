from inspect import cleandoc

import pytest

from ..aoc24 import Group, combat, parse, parse_traits, solve

sample_str = cleandoc("""
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""")


@pytest.fixture
def sample():
    return parse(sample_str)


def test_parse(sample):
    assert sample == (
        [Group(id_=1, team='Immune System', units=17, unit_hp=5390,
               weak=('radiation', 'bludgeoning'), immune=(),
               dmg=4507, dmg_type='fire', init=2),
         Group(id_=2, team='Immune System', units=989, unit_hp=1274,
               weak=('bludgeoning', 'slashing'), immune=('fire',),
               dmg=25, dmg_type='slashing', init=3)],
        [Group(id_=1, team='Infection', units=801, unit_hp=4706,
               weak=('radiation',), immune=(),
               dmg=116, dmg_type='bludgeoning', init=1),
         Group(id_=2, team='Infection', units=4485, unit_hp=2961,
               weak=('fire', 'cold'), immune=('radiation',),
               dmg=12, dmg_type='slashing', init=4)]
    )


@pytest.mark.parametrize("s, traits", (
        ('', {'weak': (), 'immune': ()}),
        ('weak to radiation',
         {'weak': ('radiation',), 'immune': ()}),
        ('weak to radiation, bludgeoning',
         {'weak': ('radiation', 'bludgeoning'), 'immune': ()}),
        ('immune to cold',
         {'weak': (), 'immune': ('cold',)}),
        ('immune to cold, radiation',
         {'weak': (), 'immune': ('cold', 'radiation')}),
        ('weak to radiation; immune to cold',
         {'weak': ('radiation',), 'immune': ('cold',)}),
        ('weak to radiation, bludgeoning; immune to cold, slashing',
         {'weak': ('radiation', 'bludgeoning'),
          'immune': ('cold', 'slashing')})
))
def test_parse_traits(s, traits):
    assert parse_traits(s) == traits


def test_combat(sample):
    assert combat(*sample) == 5216


def test_solve():
    assert solve() == (14000, 6149)
