from inspect import cleandoc

import pytest

from year2020.aoc19 import (
    count_part1,
    count_part2,
    parse,
    resolve,
    solve,
)

rules_1 = cleandoc("""
    0: 1 2
    1: "a"
    2: 1 3 | 3 1
    3: "b"

    aaa
""")

rules_2 = cleandoc("""
    0: 4 1 5
    1: 2 3 | 3 2
    2: 4 4 | 5 5
    3: 4 5 | 5 4
    4: "a"
    5: "b"

    ababbb
    bababa
    abbbab
    aaabbb
    aaaabbb
""")

rules_3 = cleandoc("""
    42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: "a"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: "b"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1

    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""")

sample_rulesets = (rules_1, rules_2, rules_3)
sample_resolved = ('a(ab|ba)', 'a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b')
sample_match_count = (0, 2, 3)


@pytest.mark.parametrize(
    'sample, result', zip(sample_rulesets, sample_resolved)
)
def test_resolve(sample: str, result: int):
    rules, _ = parse(sample)
    assert resolve(rules)[0] == result


@pytest.mark.parametrize(
    'sample, result', zip(sample_rulesets, sample_match_count)
)
def test_count_part1(sample: str, result: int):
    rules, msgs = parse(sample)
    assert count_part1(resolve(rules), msgs) == result


def test_count_part2():
    rules, msgs = parse(rules_3)
    resolved = resolve(rules)
    assert count_part2(resolved, msgs) == 12


def test_solve():
    assert solve() == (269, 403)
