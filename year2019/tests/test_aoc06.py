from year2019.aoc06 import count_min_transfers, count_orbits, parse, solve



def test_count_orbits():
    sample = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L'
    assert count_orbits(parse(sample)) == 42


def test_count_min_transfers():
    sample = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN'
    assert count_min_transfers(parse(sample)) == 4


def test_solve():
    assert solve() == (245089, 511)
