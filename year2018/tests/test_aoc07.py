from aoc07 import parse, toposort, work
from helpers import read_puzzle

sample = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip()


def test_parse():
    assert parse(sample) == {
        'in': {'A': ['C'],
               'B': ['A'],
               'D': ['A'],
               'E': ['B', 'D', 'F'],
               'F': ['C']},
        'out': {'A': ['B', 'D'],
                'B': ['E'],
                'C': ['A', 'F'],
                'D': ['E'],
                'F': ['E']}
    }


def test_toposort():
    assert ''.join(toposort(parse(sample))) == 'CABDFE'


def test_work():
    assert work(sample, 1, 0)[0] == 'CABDFE'
    assert work(sample, 2, 0) == ('CABFDE', 15)


def test_full_puzzle_old():
    graph = parse(read_puzzle())
    assert ''.join(toposort(graph)) == 'BHMOTUFLCPQKWINZVRXAJDSYEG'


def test_full_puzzle():
    puzzle = read_puzzle()
    assert work(puzzle, 1, 0)[0] == 'BHMOTUFLCPQKWINZVRXAJDSYEG'
    assert work(puzzle, 5, 60) == ('BHTUMOFLQZCPWKIVNRXASJDYEG', 877)
