import re
from collections import Counter, namedtuple
from itertools import chain, groupby
from typing import Iterable, Iterator, List, Tuple

from helpers import read_puzzle

Guard = namedtuple('Guard', 'id sleep')


def sleep_ranges(schedule: List[int]) -> List[range]:
    return [range(a, b) for a, b in zip(schedule[::2], schedule[1::2])]


def parse_journal(journal: str) -> Iterator[Guard]:
    records = sorted(journal.splitlines())
    for isNewShift, actions in groupby(records, lambda r: 'Guard' in r):
        if isNewShift:
            id_ = int(re.search(r'#(\d+)', next(actions)).group(1))
        else:
            schedule = [int(re.search(r':(\d\d)', a).group(1)) for a in actions]
            # noinspection PyUnboundLocalVariable
            yield Guard(id_, sleep_ranges(schedule))


def sum_time_asleep(guards: Iterable[Guard]) -> int:
    """The total number of minutes spent asleep by all given guards."""
    return sum(map(len, chain(*(g.sleep for g in guards))))


def get_snooziest_minute(guard_most_asleep: Iterable[Guard]) -> Tuple[int, int]:
    their_minutes = chain(*chain(*(g.sleep for g in guard_most_asleep)))
    snooziest_minute = Counter(their_minutes).most_common(1)[0]
    return snooziest_minute


def strategy1(guards: Iterable[Guard]):
    key = lambda g: g.id
    grouped = [list(gs) for _, gs in groupby(sorted(guards, key=key), key)]
    guard_most_asleep: List[Guard] = max(grouped, key=sum_time_asleep)
    snooziest_minute = get_snooziest_minute(guard_most_asleep)[0]
    return guard_most_asleep[0].id * snooziest_minute


def strategy2(guards: Iterable[Guard]):
    key = lambda g: g.id
    grouped = [list(gs) for _, gs in groupby(sorted(guards, key=key), key)]
    ids_and_sn_mins = ((g[0].id, get_snooziest_minute(g)) for g in grouped)
    top = max(ids_and_sn_mins, key=lambda x: x[1][1])
    return top[0] * top[1][0]


if __name__ == '__main__':
    guards_ = list(parse_journal(read_puzzle()))
    print(strategy1(guards_), strategy2(guards_))
