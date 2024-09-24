from collections import Counter
from inspect import cleandoc

from year2020.aoc07 import parse, resolve, solve

sample = cleandoc("""
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.
""")


def test_parse():
    assert parse(sample) == {
        'light red': Counter({'muted yellow': 2, 'bright white': 1}),
        'dark orange': Counter({'muted yellow': 4, 'bright white': 3}),
        'bright white': Counter({'shiny gold': 1}),
        'muted yellow': Counter({'faded blue': 9, 'shiny gold': 2}),
        'shiny gold': Counter({'vibrant plum': 2, 'dark olive': 1}),
        'dark olive': Counter({'dotted black': 4, 'faded blue': 3}),
        'vibrant plum': Counter({'dotted black': 6, 'faded blue': 5}),
        'faded blue': Counter(),
        'dotted black': Counter(),
    }


def test_resolve():
    assert resolve(parse(sample)) == {
        'faded blue': Counter(),
        'dotted black': Counter(),
        'dark olive': Counter({'dotted black': 4, 'faded blue': 3}),
        'vibrant plum': Counter({'dotted black': 6, 'faded blue': 5}),
        'shiny gold': Counter({
            'dotted black': 16,
            'faded blue': 13,
            'vibrant plum': 2,
            'dark olive': 1,
        }),
        'bright white': Counter({
            'dotted black': 16,
            'faded blue': 13,
            'vibrant plum': 2,
            'shiny gold': 1,
            'dark olive': 1,
        }),
        'muted yellow': Counter({
            'faded blue': 35,
            'dotted black': 32,
            'vibrant plum': 4,
            'shiny gold': 2,
            'dark olive': 2,
        }),
        'light red': Counter({
            'faded blue': 83,
            'dotted black': 80,
            'vibrant plum': 10,
            'shiny gold': 5,
            'dark olive': 5,
            'muted yellow': 2,
            'bright white': 1,
        }),
        'dark orange': Counter({
            'faded blue': 179,
            'dotted black': 176,
            'vibrant plum': 22,
            'shiny gold': 11,
            'dark olive': 11,
            'muted yellow': 4,
            'bright white': 3,
        }),
    }


def test_solve():
    assert solve() == (287, 48160)
