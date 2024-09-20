# https://adventofcode.com/2019/day/25

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


class Droid:
    def __init__(self, program: Intcode) -> None:
        self.gen = iter(Computer(program))
        self.listen()

    def listen(self, first_ch: str = ''):
        line = None
        try:
            while line != 'Command?':
                line = '' if line is not None else first_ch
                while (out := next(self.gen)) != 10:
                    line += chr(out)
                print(line)
        except StopIteration:
            pass

    def execute(self, cmd: str):
        print(f'<<< {cmd}')
        next(self.gen)
        for ch in cmd:
            self.gen.send(ord(ch))
        out = self.gen.send(10)
        self.listen(chr(out))


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    droid = Droid(program)
    commands = (
        'east',
        'east',
        'north',
        'east',
        'east',
        'take astronaut ice cream',
        'west',
        'west',
        'south',
        'west',
        'west',
        'north',
        'west',
        'take sand',
        'east',
        'south',
        'south',
        'south',
        'take mutex',
        'south',
        'take boulder',
        'east',
        'south',
        'east',
    )
    for cmd in commands:
        droid.execute(cmd)
    return 2236672, 0


if __name__ == '__main__':
    print(solve())
