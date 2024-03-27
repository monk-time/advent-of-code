from helpers import read_puzzle
from intcode import Computer, Intcode, parse

CLOCKWISE_DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
COLORS = ['.', '#']
Coord = tuple[int, int]


def add(t1: Coord, t2: Coord) -> Coord:
    return t1[0] + t2[0], t1[1] + t2[1]


def paint_panels(program: Intcode, starting_color: int = 0):
    robot_pos = (0, 0)
    robot_dir = (0, -1)
    count_painted = 0
    painted_panels: dict[Coord, int] = {(0, 0): starting_color}
    gen = iter(Computer(program))
    while True:
        try:
            next(gen)
            cur_color: int = painted_panels.get(robot_pos, 0)
            color = gen.send(cur_color)
            if robot_pos not in painted_panels:
                count_painted += 1
            painted_panels[robot_pos] = color
            delta = next(gen) * 2 - 1  # 1 -> 1, 0 -> -1
            robot_dir = CLOCKWISE_DIRS[
                (CLOCKWISE_DIRS.index(robot_dir) + delta) % 4
            ]
            robot_pos = add(robot_pos, robot_dir)
        except StopIteration:
            return painted_panels


def print_panels(panels: dict[Coord, int]):
    coords = list(panels.keys())
    xs = [t[0] for t in coords]
    ys = [t[1] for t in coords]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    field = [
        [COLORS[panels.get((x, y), 0)] for x in range(min_x, max_x + 1)]
        for y in range(min_y, max_y + 1)
    ]
    print('\n'.join(''.join(line) for line in field))


def solve() -> tuple[int, str]:
    puzzle = parse(read_puzzle())
    panels_part1 = paint_panels(puzzle)
    panels_part2 = paint_panels(puzzle, 1)
    print_panels(panels_part2)
    return len(panels_part1), 'ABEKZGFG'


if __name__ == '__main__':
    print(solve())
