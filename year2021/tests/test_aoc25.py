from inspect import cleandoc

import pytest

from year2021.aoc25 import State, find_stop, parse, solve, step

sample_1 = cleandoc("""
    ...>...
    .......
    ......>
    v.....>
    ......>
    .......
    ..vvv..
""")

sample_2 = cleandoc("""
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
""")


def state_to_str(state: State) -> str:
    return '\n'.join(
        ''.join(
            '>'
            if (i, j) in state.east
            else 'v'
            if (i, j) in state.south
            else '.'
            for j in range(state.width)
        )
        for i in range(state.height)
    )


def test_parse():
    assert state_to_str(parse(sample_1)) == sample_1
    assert state_to_str(parse(sample_2)) == sample_2


@pytest.mark.parametrize(
    'sample, result',
    (
        (
            sample_1,
            cleandoc("""
                ..vv>..
                .......
                >......
                v.....>
                >......
                .......
                ....v..
            """),
        ),
        (
            sample_2,
            cleandoc("""
                ....>.>v.>
                v.v>.>v.v.
                >v>>..>v..
                >>v>v>.>.v
                .>v.v...v.
                v>>.>vvv..
                ..v...>>..
                vv...>>vv.
                >.v.v..v.v
            """),
        ),
    ),
)
def test_step(sample: str, result: str):
    state = state_to_str(step(parse(sample)))
    assert state == result


def test_find_stop():
    assert find_stop(parse(sample_2)) == 58


def test_solve():
    assert solve() == (565, 0)
