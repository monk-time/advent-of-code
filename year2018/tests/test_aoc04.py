from aoc04 import Guard, parse_journal, strategy1, strategy2, sum_time_asleep
from helpers import read_puzzle

sample = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip()

guards = list(parse_journal(sample))


def test_parse_journal():
    assert guards == [
        Guard(id=10, sleep=[range(5, 25), range(30, 55)]),
        Guard(id=99, sleep=[range(40, 50)]),
        Guard(id=10, sleep=[range(24, 29)]),
        Guard(id=99, sleep=[range(36, 46)]),
        Guard(id=99, sleep=[range(45, 55)]),
    ]


def test_sum_time_asleep():
    assert sum_time_asleep(guards) == 80


def test_strategy1():
    assert strategy1(guards) == 240


def test_strategy2():
    assert strategy2(guards) == 4455


def test_full_puzzle():
    puzzle = list(parse_journal(read_puzzle()))
    assert strategy1(puzzle) == 26281
    assert strategy2(puzzle) == 73001
