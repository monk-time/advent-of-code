# https://adventofcode.com/2019/day/23

from collections import deque

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


def network(program: Intcode, *, disable_nat: bool = True) -> int:  # noqa: C901
    computers = [iter(Computer(program)) for _ in range(50)]
    for i, computer in enumerate(computers):
        next(computer)
        computer.send(i)
    queue = [deque() for _ in range(50)]
    nat, nat_history, queue_size = None, set(), 0
    no_active_senders, is_idle = False, False
    while True:
        if no_active_senders and queue_size == 0:
            is_idle = True
        no_active_senders = True
        for i, computer in enumerate(computers):
            idest = None  # destination instantly returned after input
            use_nat = i == 0 and is_idle and nat is not None
            while (queue[i] and idest is None) or use_nat:
                if not use_nat:
                    x, y = queue[i].popleft()
                    queue_size -= 1
                else:
                    x, y = nat  # type: ignore
                    is_idle = use_nat = False
                    if y in nat_history:
                        return y
                    nat_history.add(y)
                _, idest = computer.send(x), computer.send(y)
            while (
                dest := idest if idest is not None else computer.send(-1)
            ) is not None:
                no_active_senders = False
                idest = None
                (x, y) = computer.send(-1), computer.send(-1)
                if dest == 255:
                    if disable_nat:
                        return y
                    nat = (x, y)
                    continue
                queue[dest].append((x, y))
                queue_size += 1


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    return network(program), network(program, disable_nat=False)


if __name__ == '__main__':
    print(solve())
