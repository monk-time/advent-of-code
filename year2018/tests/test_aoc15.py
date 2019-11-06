import pytest

from aoc15 import State, Unit, play_round, replace_chars
from helpers import block_unwrap

sample = """
#######
#.G.E.#
#E.G.E#
#.G.E.#
#######
""".strip()


@pytest.fixture
def st_sample():
    return State.fromstring(sample)


@pytest.fixture
def st_cross():
    return State.fromstring(block_unwrap("""
        #####
        #.G.#
        #GEG#
        #.G.#
        #####
    """, border=False))


def test_replace_chars():
    chars = {(1, 1): '@', (1, 3): '%', (3, 5): '*', (4, 6): '&'}
    assert replace_chars(sample, chars) == block_unwrap("""
        #######
        #@G%E.#
        #E.G.E#
        #.G.E*#
        ######&
    """, border=False)


def test_state_fromstring(st_sample):
    assert st_sample.height == 5 and st_sample.width == 7
    assert st_sample.map[(0, 0)] == '#'
    assert st_sample.map[(1, 1)] == '.'
    assert st_sample.map[(1, 2)] == 'G'
    assert st_sample.map[(1, 4)] == 'E'
    assert st_sample.units == [
        Unit((1, 2), 'G'),
        Unit((1, 4), 'E'),
        Unit((2, 1), 'E'),
        Unit((2, 3), 'G'),
        Unit((2, 5), 'E'),
        Unit((3, 2), 'G'),
        Unit((3, 4), 'E')
    ]


def test_state_str(st_sample):
    assert str(st_sample) == sample
    assert st_sample.__str__(hp=True) == block_unwrap("""
        #######
        #.G.E.#   G(200), E(200)
        #E.G.E#   E(200), G(200), E(200)
        #.G.E.#   G(200), E(200)
        #######
    """, border=False)


def test_state_deepcopy_basic(st_cross):
    repr_cross = repr(st_cross)
    st_copy = st_cross.deepcopy()
    repr_copy = repr(st_copy)
    assert repr_cross == repr_copy
    assert st_cross == st_copy

    # Check that playing a round doesn't mutate the original state
    play_round(st_copy)
    assert repr_copy == repr(st_copy)
    assert repr_cross == repr(st_cross)


def test_state_deepcopy_after_death(st_cross):
    elf = next(u for u in st_cross.units if u.type == 'E')
    elf.hp = 1
    repr_cross = repr(st_cross)
    st_new = play_round(st_cross)
    assert st_new.finished
    assert len(st_new.units) < len(st_cross.units)
    assert repr_cross == repr(st_cross)


def test_state_squares_in_range(st_sample, st_cross):
    assert st_sample.squares_in_range((1, 2)) == \
           [(1, 1), (1, 3), (2, 2)]
    assert st_sample.squares_in_range((2, 3)) == \
           [(1, 3), (2, 2), (2, 4), (3, 3)]
    assert st_cross.squares_in_range((1, 2)) == [(1, 1), (1, 3)]
    assert st_cross.squares_in_range((2, 1)) == [(1, 1), (3, 1)]
    assert st_cross.squares_in_range((2, 2)) == []


def test_unit_is_enemy():
    g = Unit((1, 2), 'G')
    e1 = Unit((2, 2), 'E')
    e2 = Unit((2, 2), 'E')
    assert g.is_enemy(e1)
    assert not e1.is_enemy(e2)


def test_unit_is_in_range():
    """
        012
        345
        678
    """
    us = State.fromstring('EEE\nEEE\nEEE').units
    all_in_range = lambda n: [u for u in us if u.is_in_range(us[n])]
    assert all_in_range(0) == [us[1], us[3]]
    assert all_in_range(2) == [us[1], us[5]]
    assert all_in_range(6) == [us[3], us[7]]
    assert all_in_range(8) == [us[5], us[7]]
    assert all_in_range(1) == [us[0], us[2], us[4]]
    assert all_in_range(3) == [us[0], us[4], us[6]]
    assert all_in_range(5) == [us[2], us[4], us[8]]
    assert all_in_range(7) == [us[4], us[6], us[8]]
    assert all_in_range(4) == [us[1], us[3], us[5], us[7]]


def test_play_round_no_moves(st_cross):
    # Check target selection in reading order
    st = st_cross
    st = play_round(st)
    assert st.__str__(hp=True) == block_unwrap("""
        #####
        #.G.#   G(197)
        #GEG#   G(200), E(188), G(200)
        #.G.#   G(200)
        #####
    """, border=False)

    # Check that reachable targets with the lowest hp have priority
    st = State.fromstring(block_unwrap("""
        ######
        #.G..#
        #GEGE#
        #.GE.#
        ######
    """, border=False))

    st = play_round(st)
    assert st.__str__(hp=True) == block_unwrap("""
        ######
        #.G..#   G(197)
        #GEGE#   G(200), E(188), G(194), E(200)
        #.GE.#   G(200), E(200)
        ######
    """, border=False)

    st = play_round(st)
    assert st.__str__(hp=True) == block_unwrap("""
        ######
        #.G..#   G(197)
        #GEGE#   G(200), E(176), G(185), E(200)
        #.GE.#   G(200), E(200)
        ######
    """, border=False)

    for _ in range(15):
        st = play_round(st)
    # Last round before anyone can move
    assert st.__str__(hp=True) == block_unwrap("""
        ######
        #.G..#   G(197)
        #G.GE#   G(200), G(50), E(200)
        #.GE.#   G(200), E(197)
        ######
    """, border=False)


def test_play_round_played_rounds(st_cross):
    while not st_cross.finished:
        st_cross = play_round(st_cross)
    # 200 = 16 * 4 * 3 + 8, combat ends before the last goblin can act
    assert st_cross.rounds_played == 16
