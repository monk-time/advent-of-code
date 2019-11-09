from inspect import cleandoc
from typing import List

from aoc13 import Cart, emulate, look_ahead, move, next_tick, parse, solve

sample = cleandoc(r"""
    /->-\        
    |   |  /----\
    | /-+--+-\  |
    | | |  | v  |
    \-+-/  \-+--/
      \------/   
""")

sample2 = cleandoc(r"""
    />-<\  
    |   |  
    | /<+-\
    | | | v
    \>+</ |
      |   ^
      \<->/
""")


def test_parse():
    carts, tracks = parse(sample)
    assert carts == [Cart(x=2, y=0, dir='>', turn=0), Cart(x=9, y=3, dir='v', turn=0)]
    assert '\n'.join(tracks) == cleandoc(r"""
        /---\        
        |   |  /----\
        | /-+--+-\  |
        | | |  | |  |
        \-+-/  \-+--/
          \------/   
    """)


def test_look_ahead():
    assert look_ahead(Cart(x=1, y=2, dir='>', turn=0)) == (2, 2)
    assert look_ahead(Cart(x=1, y=2, dir='<', turn=0)) == (0, 2)
    assert look_ahead(Cart(x=1, y=2, dir='^', turn=0)) == (1, 1)
    assert look_ahead(Cart(x=1, y=2, dir='v', turn=0)) == (1, 3)


def test_move_straight():
    assert move(Cart(x=1, y=2, dir='>', turn=0), '-') == Cart(2, 2, '>', 0)
    assert move(Cart(x=1, y=2, dir='<', turn=1), '-') == Cart(0, 2, '<', 1)
    assert move(Cart(x=1, y=2, dir='^', turn=2), '|') == Cart(1, 1, '^', 2)
    assert move(Cart(x=1, y=2, dir='v', turn=0), '|') == Cart(1, 3, 'v', 0)


def test_move_clockwise_turn():
    assert move(Cart(x=1, y=2, dir='^', turn=0), '/') == Cart(1, 1, '>', 0)
    assert move(Cart(x=1, y=2, dir='>', turn=1), '\\') == Cart(2, 2, 'v', 1)
    assert move(Cart(x=1, y=2, dir='v', turn=2), '/') == Cart(1, 3, '<', 2)
    assert move(Cart(x=1, y=2, dir='<', turn=0), '\\') == Cart(0, 2, '^', 0)


def test_move_counterclockwise_turn():
    assert move(Cart(x=1, y=2, dir='>', turn=0), '/') == Cart(2, 2, '^', 0)
    assert move(Cart(x=1, y=2, dir='^', turn=1), '\\') == Cart(1, 1, '<', 1)
    assert move(Cart(x=1, y=2, dir='<', turn=2), '/') == Cart(0, 2, 'v', 2)
    assert move(Cart(x=1, y=2, dir='v', turn=0), '\\') == Cart(1, 3, '>', 0)


def test_move_intersection_straight():
    assert move(Cart(x=1, y=2, dir='>', turn=1), '+') == Cart(2, 2, '>', 2)
    assert move(Cart(x=1, y=2, dir='^', turn=1), '+') == Cart(1, 1, '^', 2)
    assert move(Cart(x=1, y=2, dir='<', turn=1), '+') == Cart(0, 2, '<', 2)
    assert move(Cart(x=1, y=2, dir='v', turn=1), '+') == Cart(1, 3, 'v', 2)


def test_move_intersection_clockwise_turn():
    assert move(Cart(x=1, y=2, dir='^', turn=2), '+') == Cart(1, 1, '>', 0)
    assert move(Cart(x=1, y=2, dir='>', turn=2), '+') == Cart(2, 2, 'v', 0)
    assert move(Cart(x=1, y=2, dir='v', turn=2), '+') == Cart(1, 3, '<', 0)
    assert move(Cart(x=1, y=2, dir='<', turn=2), '+') == Cart(0, 2, '^', 0)


def test_move_intersection_counterclockwise_turn():
    assert move(Cart(x=1, y=2, dir='>', turn=0), '+') == Cart(2, 2, '^', 1)
    assert move(Cart(x=1, y=2, dir='^', turn=0), '+') == Cart(1, 1, '<', 1)
    assert move(Cart(x=1, y=2, dir='<', turn=0), '+') == Cart(0, 2, 'v', 1)
    assert move(Cart(x=1, y=2, dir='v', turn=0), '+') == Cart(1, 3, '>', 1)


def state_to_str(carts: List[Cart], tracks: List[str]) -> str:
    tracks = tracks.copy()
    for c in carts:
        tracks[c.y] = tracks[c.y][:c.x] + c.dir + tracks[c.y][c.x + 1:]
    return '\n'.join(tracks)


def test_state_to_str():
    assert state_to_str(*parse(sample)) == sample
    assert state_to_str(*parse(sample2)) == sample2


def test_next_tick_sample():
    carts, tracks, crashes = next_tick(*parse(sample))
    assert crashes == []
    assert state_to_str(carts, tracks) == cleandoc(r"""
        /-->\        
        |   |  /----\
        | /-+--+-\  |
        | | |  | |  |
        \-+-/  \->--/
          \------/   
    """)


def test_next_tick_sample2():
    carts, tracks, crashes = next_tick(*parse(sample2))
    assert crashes == [(2, 0), (2, 4), (6, 4)]
    assert state_to_str(carts, tracks) == cleandoc(r"""
        /---\  
        |   |  
        | v-+-\
        | | | |
        \-+-/ |
          |   |
          ^---^
    """)


def test_emulate():
    assert list(emulate(*parse(sample))) == ['7,3', '']
    assert list(emulate(*parse(sample2))) == ['2,0', '6,4']


def test_solve():
    assert solve() == ('16,45', '21,91')
