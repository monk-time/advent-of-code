from inspect import cleandoc

from year2021.aoc23 import expand, min_energy_to_organize, parse, solve

sample = cleandoc("""
    #############
    #...........#
    ###B#C#B#D###
      #A#D#C#A#
      #########
""")


def test_min_energy_to_organize():
    assert min_energy_to_organize(parse(sample)) == 12521


def test_min_energy_to_organize_expanded():
    assert min_energy_to_organize(expand(parse(sample))) == 44169


def test_solve():
    assert solve() == (11320, 49532)
