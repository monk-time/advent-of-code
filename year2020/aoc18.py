# https://adventofcode.com/2020/day/18

from collections.abc import Iterable
from functools import partial
from operator import add, mul

from helpers import read_puzzle

type Tokens = Iterable[int | str]
type Precedence = dict[str, int]

OPS = {'+': add, '*': mul}


def parse(s: str) -> list[Tokens]:
    return [parse_tokens(line) for line in s.split('\n')]


def parse_tokens(s: str) -> Tokens:
    return [int(ch) if ch.isdigit() else ch for ch in s if ch != ' ']


def infix_to_postfix(tokens: Tokens, precedence: Precedence) -> Tokens:
    # Shunting yard algorithm
    stack: list[str] = []

    for token in tokens:
        if isinstance(token, int):
            yield token
        elif token in precedence:
            while (
                stack
                and stack[-1] != '('
                and precedence[stack[-1]] <= precedence[token]
            ):
                yield stack.pop()
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                yield stack.pop()
            stack.pop()  # remove '('

    while stack:
        yield stack.pop()


def calc_postfix(postfix: Tokens) -> int:
    stack = []
    for token in postfix:
        if isinstance(token, int):
            stack.append(token)
        else:
            op = OPS[token]
            stack.append(op(stack.pop(), stack.pop()))
    return stack[0]


def calc(expr: Tokens, precedence: Precedence) -> int:
    return calc_postfix(infix_to_postfix(expr, precedence))


calc_1 = partial(calc, precedence={'+': 1, '*': 1})
calc_2 = partial(calc, precedence={'+': 1, '*': 2})


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    return sum(map(calc_1, puzzle)), sum(map(calc_2, puzzle))


if __name__ == '__main__':
    print(solve())
