from inspect import cleandoc

import pytest

from year2021.aoc10 import (
    Result,
    check_brackets,
    completion_score,
    parse,
    solve,
    syntax_score,
)

sample = cleandoc("""
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
""")

sample_results = (
    {'type': 'incomplete', 'data': '}}]])})]'},
    {'type': 'incomplete', 'data': ')}>]})'},
    {'type': 'corrupted', 'data': '}'},
    {'type': 'incomplete', 'data': '}}>}>))))'},
    {'type': 'corrupted', 'data': ')'},
    {'type': 'corrupted', 'data': ']'},
    {'type': 'incomplete', 'data': ']]}}]}]}>'},
    {'type': 'corrupted', 'data': ')'},
    {'type': 'corrupted', 'data': '>'},
    {'type': 'incomplete', 'data': '])}>'},
)


@pytest.fixture(scope='module')
def results() -> list[Result]:
    return [check_brackets(line) for line in parse(sample)]


@pytest.mark.parametrize('line, result', zip(parse(sample), sample_results))
def test_check_brackets(line: str, result: Result):
    assert check_brackets(line) == result


def test_syntax_score(results: list[Result]):
    assert syntax_score(results) == 26397


def test_completion_score(results: list[Result]):
    assert completion_score(results) == 288957


def test_solve():
    assert solve() == (392421, 2769449099)
