# https://adventofcode.com/2021/day/2
# tags: #instructions #reduce

import re
from functools import reduce
from typing import TYPE_CHECKING, Literal, TypedDict, cast

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

type Coord = tuple[int, int]
type Dir = Literal['forward', 'down', 'up']


class Command(TypedDict):
    dir: Dir
    n: int


class Sub(TypedDict):
    pos: Coord
    aim: int


RE_COMMAND = r'^(?P<dir>forward|down|up) (?P<n>\d+)$'


def parse(s: str) -> Iterable[Command]:
    for line in s.splitlines():
        if not (m := re.match(RE_COMMAND, line)):
            raise ValueError
        d = m.groupdict()
        d['n'] = int(d['n'])
        yield cast('Command', d)


def execute(sub: Sub, command: Command) -> Sub:
    x, y, aim = *sub['pos'], sub['aim']
    n = command['n']
    match command['dir']:
        case 'forward':
            return Sub(pos=(x + n, y + n * aim), aim=aim)
        case 'down':
            return Sub(pos=(x, y), aim=aim + n)
        case 'up':
            return Sub(pos=(x, y), aim=aim - n)


def travel(commands: Iterable[Command], *, with_aim: bool = False) -> int:
    sub = reduce(execute, commands, Sub(pos=(0, 0), aim=0))
    x, y, aim = *sub['pos'], sub['aim']
    return x * y if with_aim else x * aim


def solve() -> tuple[int, int]:
    commands = list(parse(read_puzzle()))
    return travel(commands), travel(commands, with_aim=True)


if __name__ == '__main__':
    print(solve())
