from inspect import cleandoc

from year2020.aoc16 import (
    TicketData,
    calc_ticket_scanning_error_rate,
    parse,
    solve,
)

input_1 = cleandoc("""
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
""")

input_2 = cleandoc("""
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
""")


def test_parse():
    assert parse(input_1) == TicketData(
        rules=(((1, 3), (5, 7)), ((6, 11), (33, 44)), ((13, 40), (45, 50))),
        ticket=(7, 1, 14),
        tickets=((7, 3, 47), (40, 4, 50), (55, 2, 20), (38, 6, 12)),
    )


def test_calc_ticket_scanning_error_rate():
    assert calc_ticket_scanning_error_rate(parse(input_1)) == 71


def test_solve():
    assert solve() == (27850, 491924517533)
