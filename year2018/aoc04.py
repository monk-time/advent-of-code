# https://adventofcode.com/2018/day/4

import re
from collections import Counter, defaultdict
from itertools import chain, groupby
from operator import itemgetter

from helpers import read_puzzle

Naps = list[range]
Guards = dict[int, Naps]


def sleep_ranges(schedule: list[int]) -> Naps:
    return list(map(range, schedule[::2], schedule[1::2], strict=True))


def parse_journal(journal: str) -> Guards:
    records = sorted(journal.splitlines())
    guards = defaultdict(list)
    for is_new_shift, actions in groupby(records, lambda r: 'Guard' in r):
        if is_new_shift:
            id_ = int(re.search(r'#(\d+)', next(actions)).group(1))  # type: ignore
        else:
            schedule = [
                int(re.search(r':(\d\d)', a).group(1))  # type: ignore
                for a in actions
            ]
            guards[id_].extend(sleep_ranges(schedule))
    return guards


def total_time_asleep(naps: Naps) -> int:
    """Get the total number of minutes spent asleep by a given guard."""
    return sum(map(len, naps))


def snooziest_minute(naps: Naps) -> tuple[int, int]:
    """Find the minute during which the guard is most often asleep."""
    return Counter(chain(*naps)).most_common(1)[0]


def strategy1(guards: Guards):
    most_asleep: int = max(guards, key=lambda g: total_time_asleep(guards[g]))
    minute = snooziest_minute(guards[most_asleep])[0]
    return most_asleep * minute


def strategy2(guards: Guards):
    stats = [(g, *snooziest_minute(guards[g])) for g in guards]
    guard, minute, *_ = max(stats, key=itemgetter(2))
    return guard * minute


def solve():
    guards = parse_journal(read_puzzle())
    return strategy1(guards), strategy2(guards)


if __name__ == '__main__':
    print(solve())
