# https://adventofcode.com/2020/day/16

import re
from dataclasses import dataclass
from functools import partial
from itertools import batched, chain, pairwise
from math import prod

from helpers import read_puzzle

type Range = tuple[int, int]
type Fields = tuple[int, ...]
type Rule = tuple[Range, Range]
type Rules = tuple[Rule, ...]


@dataclass(frozen=True)
class TicketData:
    rules: Rules
    ticket: Fields
    tickets: tuple[Fields, ...]


def parse(s: str) -> TicketData:
    parts = s.split('\n\n')
    find_ints = lambda arr: map(int, re.findall(r'\d+', arr))
    rules: Rules = tuple(
        batched(batched(find_ints(parts[0]), 2, strict=True), 2, strict=True)
    )  # type: ignore
    ticket = tuple(find_ints(parts[1]))
    tickets = tuple(
        tuple(find_ints(line)) for line in parts[2].split('\n')[1:]
    )
    return TicketData(rules, ticket, tickets)


def matches_rule(rule: Rule, n: int) -> bool:
    (a1, a2), (b1, b2) = rule
    return a1 <= n <= a2 or b1 <= n <= b2


def is_invalid_field(rules: Rules, n: int) -> bool:
    return not any(matches_rule(rule, n) for rule in rules)


def find_invalid_fields(rules: Rules, ticket: Fields) -> Fields:
    return tuple(n for n in ticket if is_invalid_field(rules, n))


def calc_ticket_scanning_error_rate(td: TicketData) -> int:
    func = partial(find_invalid_fields, td.rules)
    return sum(chain(*map(func, td.tickets)))


def find_candidate_cols(
    rule: Rule, tickets: tuple[Fields, ...]
) -> tuple[int, ...]:
    return tuple(
        i
        for i in range(len(tickets[0]))
        if all(matches_rule(rule, t[i]) for t in tickets)
    )


def mul_departure_fields(td: TicketData) -> int:
    valid_tickets = tuple(
        t
        for t in chain([td.ticket], td.tickets)
        if not find_invalid_fields(td.rules, t)
    )
    candidates = sorted(
        (
            (rule_idx, find_candidate_cols(td.rules[rule_idx], valid_tickets))
            for rule_idx in range(len(td.rules))
        ),
        key=lambda t: len(t[1]),
    )
    rule_idx, cols = candidates[0]
    rule_cols: list[int] = [0] * len(td.rules)
    rule_cols[rule_idx] = cols[0]
    # Assumption: there's no branching
    # and the number of candidates strictly increases
    for (_, prev), (rule_idx, cols) in pairwise(candidates):
        rule_cols[rule_idx] = next(iter(set(cols) - set(prev)))
    return prod(td.ticket[col] for col in rule_cols[:6])


def solve() -> tuple[int, int]:
    td = parse(read_puzzle())
    return calc_ticket_scanning_error_rate(td), mul_departure_fields(td)


if __name__ == '__main__':
    print(solve())
