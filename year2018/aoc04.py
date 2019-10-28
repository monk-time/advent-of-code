import re
from collections import Counter, defaultdict
from itertools import chain, groupby
from typing import Dict, List, Tuple

from helpers import read_puzzle

Naps = List[range]
Guards = Dict[int, Naps]


def sleep_ranges(schedule: List[int]) -> Naps:
    return [range(a, b) for a, b in zip(schedule[::2], schedule[1::2])]


def parse_journal(journal: str) -> Guards:
    records = sorted(journal.splitlines())
    guards = defaultdict(list)
    for isNewShift, actions in groupby(records, lambda r: 'Guard' in r):
        if isNewShift:
            id_ = int(re.search(r'#(\d+)', next(actions)).group(1))
        else:
            schedule = [int(re.search(r':(\d\d)', a).group(1)) for a in actions]
            # noinspection PyUnboundLocalVariable
            guards[id_].extend(sleep_ranges(schedule))
    return guards


def sum_time_asleep(naps: Naps) -> int:
    """Get the total number of minutes spent asleep by a given guard."""
    return sum(map(len, naps))


def get_snooziest_minute(naps: Naps) -> Tuple[int, int]:
    """Find the minute during which the guard is most often asleep."""
    return Counter(chain(*naps)).most_common(1)[0]


def strategy1(guards: Guards):
    most_asleep: int = max(guards, key=lambda g: sum_time_asleep(guards[g]))
    minute = get_snooziest_minute(guards[most_asleep])[0]
    return most_asleep * minute


def strategy2(guards: Guards):
    ids_and_sn_mins = ((g, get_snooziest_minute(guards[g])) for g in guards)
    top = max(ids_and_sn_mins, key=lambda x: x[1][1])
    return top[0] * top[1][0]


def solve():
    guards = parse_journal(read_puzzle())
    return strategy1(guards), strategy2(guards)


if __name__ == '__main__':
    print(solve())
