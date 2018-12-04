from aoc04 import get_snooziest_minute, parse_journal, strategy1, strategy2, sum_time_asleep
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

guards = parse_journal(sample)


def test_parse_journal():
    assert guards == {
        10: [range(5, 25), range(30, 55), range(24, 29)],
        99: [range(40, 50), range(36, 46), range(45, 55)],
    }


def test_sum_time_asleep():
    assert [sum_time_asleep(g) for g in guards.values()] == [50, 30]


def test_get_snooziest_minute():
    assert get_snooziest_minute(guards[10]) == (24, 2)
    assert get_snooziest_minute(guards[99]) == (45, 3)


def test_strategy1():
    assert strategy1(guards) == 240


def test_strategy2():
    assert strategy2(guards) == 4455


def test_full_puzzle():
    puzzle = parse_journal(read_puzzle())
    assert strategy1(puzzle) == 26281
    assert strategy2(puzzle) == 73001
