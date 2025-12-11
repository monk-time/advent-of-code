from inspect import cleandoc

import pytest

from utils_proxy import read_puzzle
from year2021.aoc24 import execute, execute_decoded, parse, solve

sample = cleandoc("""
""")


@pytest.mark.parametrize(
    'program, input_vals, result',
    (
        (
            cleandoc("""
                inp x
                mul x -1
            """),
            (1,),
            [0, -1, 0, 0],
        ),
        (
            cleandoc("""
                inp z
                inp x
                mul z 3
                eql z x
            """),
            (2, 6),
            [0, 6, 0, 1],
        ),
        (
            cleandoc("""
                inp w
                add z w
                mod z 2
                div w 2
                add y w
                mod y 2
                div w 2
                add x w
                mod x 2
                div w 2
                mod w 2
            """),
            (10,),
            [1, 0, 1, 0],
        ),
    ),
)
def test_execute(program: str, input_vals: tuple[int, ...], result: list[int]):
    assert execute(parse(program), input_vals) == result


def test_execute_decoded():
    program = parse(read_puzzle(24, 2021))
    for n in range(1000):
        input_vals = tuple(int(ch) for ch in str(n).zfill(14))
        assert execute(program, input_vals) == execute_decoded(input_vals)


def test_solve():
    assert solve() == (79997391969649, 16931171414113)
