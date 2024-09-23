# https://adventofcode.com/2020/day/4

import re
from collections.abc import Callable

from helpers import read_puzzle

type Passport = dict[str, str]


def is_year_in_range(s: str, n: int, m: int) -> bool:
    return len(s) == 4 and s.isdigit() and n <= int(s) <= m


REQ_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
EYE_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
RE_HEIGHT = re.compile(r'^(\d+)(cm|in)$')
RE_HAIR_COLOR = re.compile(r'^#[0-9a-f]{6}$')
VALIDATORS: dict[str, Callable[[str], bool]] = {
    'byr': lambda s: is_year_in_range(s, 1920, 2002),
    'iyr': lambda s: is_year_in_range(s, 2010, 2020),
    'eyr': lambda s: is_year_in_range(s, 2020, 2030),
    'hgt': lambda s: (
        (m := RE_HEIGHT.match(s)) is not None
        and (
            (m[2] == 'cm' and 150 <= int(m[1]) <= 193)
            or (m[2] == 'in' and 59 <= int(m[1]) <= 76)
        )
    ),
    'hcl': lambda s: RE_HAIR_COLOR.match(s) is not None,
    'ecl': lambda s: s in EYE_COLORS,
    'pid': lambda s: len(s) == 9 and s.isdigit(),
    'cid': lambda _: True,
}


def parse(s: str) -> list[Passport]:
    return [
        dict(field.split(':') for field in passport.split())
        for passport in s.split('\n\n')
    ]


def has_keys(passport: Passport) -> bool:
    return passport.keys() >= REQ_FIELDS


def is_valid(passport: Passport) -> bool:
    return has_keys(passport) and all(
        VALIDATORS[k](v) for k, v in passport.items()
    )


def solve() -> tuple[int, int]:
    passports = parse(read_puzzle())
    return sum(map(has_keys, passports)), sum(map(is_valid, passports))


if __name__ == '__main__':
    print(solve())
