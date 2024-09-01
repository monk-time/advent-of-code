from inspect import cleandoc

import pytest

from year2018.aoc15 import State, Unit, outcome, play_round, solve


def test_unit_is_enemy():
    g = Unit((1, 2), 'G')
    e1 = Unit((2, 2), 'E')
    e2 = Unit((2, 2), 'E')
    assert g.is_enemy(e1)
    assert not e1.is_enemy(e2)


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
    return State.fromstring(
        cleandoc("""
            #####
            #.G.#
            #GEG#
            #.G.#
            #####
        """)
    )


@pytest.fixture
def st_move1():
    return State.fromstring(
        cleandoc("""
            #######
            #E..G.#
            #...#.#
            #.G.#G#
            #######
        """)
    )


@pytest.fixture
def st_move2():
    return State.fromstring(
        cleandoc("""
            #######
            #.E...#
            #.....#
            #...G.#
            #######
        """)
    )


@pytest.fixture
def st_move_big():
    return State.fromstring(
        cleandoc("""
            #########
            #G..G..G#
            #.......#
            #.......#
            #G..E..G#
            #.......#
            #.......#
            #G..G..G#
            #########
        """)
    )


def test_state_fromstring(st_sample):
    assert st_sample.height == 5
    assert st_sample.width == 7
    assert st_sample.map[0, 0] == '#'
    assert st_sample.map[1, 1] == '.'
    assert st_sample.map[1, 2] == Unit((1, 2), 'G')
    assert st_sample.map[1, 4] == Unit((1, 4), 'E')
    assert st_sample.units == [
        Unit((1, 2), 'G'),
        Unit((1, 4), 'E'),
        Unit((2, 1), 'E'),
        Unit((2, 3), 'G'),
        Unit((2, 5), 'E'),
        Unit((3, 2), 'G'),
        Unit((3, 4), 'E'),
    ]


def test_state_str(st_sample):
    assert str(st_sample) == sample
    assert st_sample.__str__(hp=True) == cleandoc("""
        #######
        #.G.E.#   G(200), E(200)
        #E.G.E#   E(200), G(200), E(200)
        #.G.E.#   G(200), E(200)
        #######
    """)


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


def test_state_targets_in_range(st_cross, st_move1):
    g1, g2, e, g3, g4 = st_cross.units
    assert st_cross.targets_in_range(g1) == [e]
    assert st_cross.targets_in_range(e) == [g1, g2, g3, g4]

    u = st_move1.units[0]
    assert st_move1.targets_in_range(u) == []


def test_state_find_path(st_move1, st_move2, st_move_big):
    e = st_move1.units[0]
    assert st_move1.find_path(e) == (1, 2)
    g = st_move1.units[2]
    assert st_move1.find_path(g) == (2, 2)
    g = st_move1.units[3]
    assert st_move1.find_path(g) is None

    e, g = st_move2.units
    assert st_move2.find_path(e) == (1, 3)
    assert st_move2.find_path(g) == (2, 4)

    g = st_move_big.units[3]
    assert st_move_big.find_path(g) == (4, 2)


def test_state_move(st_move1):
    unit, _targets = st_move1.units[0], st_move1.units[1:]
    st_move1.move(unit)
    assert str(st_move1) == cleandoc("""
        #######
        #.E.G.#
        #...#.#
        #.G.#G#
        #######
    """)


def test_state_move_tricky():
    st = State.fromstring(
        cleandoc("""
            #######
            ###...#
            ###.#.#
            #.E.#.#
            #.###G#
            #.....#
            #######
        """)
    )
    e, _g = st.units
    st.move(e)
    assert str(st) == cleandoc("""
        #######
        ###...#
        ###.#.#
        #..E#.#
        #.###G#
        #.....#
        #######
    """)


def test_state_move_all(st_move_big):
    st = play_round(st_move_big)
    assert str(st) == cleandoc("""
        #########
        #.G...G.#
        #...G...#
        #...E..G#
        #.G.....#
        #.......#
        #G..G..G#
        #.......#
        #########
    """)

    st = play_round(st)
    assert str(st) == cleandoc("""
        #########
        #..G.G..#
        #...G...#
        #.G.E.G.#
        #.......#
        #G..G..G#
        #.......#
        #.......#
        #########
    """)

    st = play_round(st)
    assert str(st) == cleandoc("""
        #########
        #.......#
        #..GGG..#
        #..GEG..#
        #G..G...#
        #......G#
        #.......#
        #.......#
        #########
    """)


def test_state_hit(st_sample):
    target = st_sample.units[0]
    st_sample.hit(target, dmg=3)
    assert target.hp == 197

    st_sample.hit(target, dmg=200)
    assert target not in st_sample.units
    assert target.hp == 0


def test_state_hash(st_move2):
    assert st_move2.hash() == 0
    st = play_round(st_move2)
    assert st.hash() == 200 * 2


def test_state_elfs_alive(st_sample):
    assert st_sample.elfs_alive() == 4


def test_play_round_no_moves(st_cross):
    # Check target selection in reading order
    st = st_cross
    st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #####
        #.G.#   G(197)
        #GEG#   G(200), E(188), G(200)
        #.G.#   G(200)
        #####
    """)

    # Check that reachable targets with the lowest hp have priority
    st = State.fromstring(
        cleandoc("""
            ######
            #.G..#
            #GEGE#
            #.GE.#
            ######
        """)
    )

    st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        ######
        #.G..#   G(197)
        #GEGE#   G(200), E(188), G(194), E(200)
        #.GE.#   G(200), E(200)
        ######
    """)

    st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        ######
        #.G..#   G(197)
        #GEGE#   G(200), E(176), G(185), E(200)
        #.GE.#   G(200), E(200)
        ######
    """)

    for _ in range(15):
        st = play_round(st)
    # Last round before anyone can move
    assert st.__str__(hp=True) == cleandoc("""
        ######
        #.G..#   G(197)
        #G.GE#   G(200), G(50), E(200)
        #.GE.#   G(200), E(197)
        ######
    """)


def test_play_round_played_rounds(st_cross):
    while not st_cross.finished:
        st_cross = play_round(st_cross)
    # 200 = 16 * 4 * 3 + 8, combat ends before the last goblin can act
    assert st_cross.rounds_played == 16


samples = [
    """
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######
    """,
    """
        #######
        #G..#E#
        #E#E.E#
        #G.##.#
        #...#E#
        #...E.#
        #######
    """,
    """
        #######
        #E..EG#
        #.#G.E#
        #E.##E#
        #G..#.#
        #..E#.#
        #######
    """,
    """
        #######
        #E.G#.#
        #.#G..#
        #G.#.G#
        #G..#.#
        #...E.#
        #######
    """,
    """
        #######
        #.E...#
        #.#..G#
        #.###.#
        #E#G#G#
        #...#G#
        #######
    """,
    """
        #########
        #G......#
        #.E.#...#
        #..##..G#
        #...##..#
        #...#...#
        #.G...G.#
        #.....G.#
        #########
    """,
]

outcomes1 = [27730, 36334, 39514, 27755, 28944, 18740]
outcomes2 = [4988, 29064, 31284, 3478, 6474, 1140]


def test_play_round_full():
    st = State.fromstring(cleandoc(samples[0]))

    st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #######
        #..G..#   G(200)
        #...EG#   E(197), G(197)
        #.#G#G#   G(200), G(197)
        #...#E#   E(197)
        #.....#
        #######
    """)

    st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #######
        #...G.#   G(200)
        #..GEG#   G(200), E(188), G(194)
        #.#.#G#   G(194)
        #...#E#   E(194)
        #.....#
        #######
    """)

    while st.rounds_played != 23:
        st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #######
        #...G.#   G(200)
        #..G.G#   G(200), G(131)
        #.#.#G#   G(131)
        #...#E#   E(131)
        #.....#
        #######
    """)

    while st.rounds_played != 28:
        st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #######
        #G....#   G(200)
        #.G...#   G(131)
        #.#.#G#   G(116)
        #...#E#   E(113)
        #....G#   G(200)
        #######
    """)

    while not st.finished:
        st = play_round(st)
    assert st.__str__(hp=True) == cleandoc("""
        #######
        #G....#   G(200)
        #.G...#   G(131)
        #.#.#G#   G(59)
        #...#.#
        #....G#   G(200)
        #######
    """)
    assert st.rounds_played == 47
    assert st.hash() == outcomes1[0]


@pytest.mark.parametrize('puzzle, num_outcome', zip(samples, outcomes1))
def test_outcome(puzzle, num_outcome):
    assert outcome(cleandoc(puzzle)) == num_outcome


@pytest.mark.parametrize('puzzle, num_outcome', zip(samples, outcomes2))
def test_outcome_part2(puzzle, num_outcome):
    assert outcome(cleandoc(puzzle), force_elf_victory=True) == num_outcome


def test_solve():
    assert solve() == (191575, 75915)
