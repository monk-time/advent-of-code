from aoc10 import Point, dimensions, move_all, parse, points_to_str, solve
from helpers import block_unwrap

sample = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip()
points = parse(sample)


def test_parse():
    assert points == [
        Point(9, 1, 0, 2),
        Point(7, 0, -1, 0),
        Point(3, -2, -1, 1),
        Point(6, 10, -2, -1),
        Point(2, -4, 2, 2),
        Point(-6, 10, 2, -2),
        Point(1, 8, 1, -1),
        Point(1, 7, 1, 0),
        Point(-3, 11, 1, -2),
        Point(7, 6, -1, -1),
        Point(-2, 3, 1, 0),
        Point(-4, 3, 2, 0),
        Point(10, -3, -1, 1),
        Point(5, 11, 1, -2),
        Point(4, 7, 0, -1),
        Point(8, -2, 0, 1),
        Point(15, 0, -2, 0),
        Point(1, 6, 1, 0),
        Point(8, 9, 0, -1),
        Point(3, 3, -1, 1),
        Point(0, 5, 0, -1),
        Point(-2, 2, 2, 0),
        Point(5, -2, 1, 2),
        Point(1, 4, 2, 1),
        Point(-2, 7, 2, -2),
        Point(3, 6, -1, -1),
        Point(5, 0, 1, 0),
        Point(-6, 0, 2, 0),
        Point(5, 9, 1, -2),
        Point(14, 7, -2, 0),
        Point(-3, 6, 2, -1)
    ]


def test_dimensions():
    assert dimensions(points) == (22, 16, -6, -4)


def test_points_to_str():
    assert points_to_str(points).splitlines() == block_unwrap(r"""
        ┌──────────────────────┐
        │........#.............│
        │................#.....│
        │.........#.#..#.......│
        │......................│
        │#..........#.#.......#│
        │...............#......│
        │....#.................│
        │..#.#....#............│
        │.......#..............│
        │......#...............│
        │...#...#.#...#........│
        │....#..#..#.........#.│
        │.......#..............│
        │...........#..#.......│
        │#...........#.........│
        │...#.......#..........│
        └──────────────────────┘
    """, border=True)


def test_move_all():
    result = lambda ps: points_to_str(ps).splitlines()

    points2 = move_all(points)
    assert result(points2) == block_unwrap(r"""
        ┌──────────────────┐
        │........#....#....│
        │......#.....#.....│
        │#.........#......#│
        │..................│
        │....#.............│
        │..##.........#....│
        │....#.#...........│
        │...##.##..#.......│
        │......#.#.........│
        │......#...#.....#.│
        │#...........#.....│
        │..#.....#.#.......│
        └──────────────────┘
    """, border=True)

    points3 = move_all(points2)
    assert result(points3) == block_unwrap(r"""
        ┌──────────────┐
        │..........#...│
        │#..#...####..#│
        │..............│
        │....#....#....│
        │..#.#.........│
        │...#...#......│
        │...#..#..#.#..│
        │#....#.#......│
        │.#...#...##.#.│
        │....#.........│
        └──────────────┘
    """, border=True)

    points4 = move_all(points3)
    assert result(points4) == block_unwrap(r"""
        ┌──────────┐
        │#...#..###│
        │#...#...#.│
        │#...#...#.│
        │#####...#.│
        │#...#...#.│
        │#...#...#.│
        │#...#...#.│
        │#...#..###│
        └──────────┘
    """, border=True)


def test_solve():
    result, sec = solve()
    assert result.splitlines() == block_unwrap(r"""
        ┌──────────────────────────────────────────────────────────────┐
        │######.....###..#....#..#....#...####....####...#....#..#....#│
        │#...........#...#....#..##...#..#....#..#....#..##...#..#....#│
        │#...........#....#..#...##...#..#.......#.......##...#...#..#.│
        │#...........#....#..#...#.#..#..#.......#.......#.#..#...#..#.│
        │#####.......#.....##....#.#..#..#.......#.......#.#..#....##..│
        │#...........#.....##....#..#.#..#.......#.......#..#.#....##..│
        │#...........#....#..#...#..#.#..#.......#.......#..#.#...#..#.│
        │#.......#...#....#..#...#...##..#.......#.......#...##...#..#.│
        │#.......#...#...#....#..#...##..#....#..#....#..#...##..#....#│
        │######...###....#....#..#....#...####....####...#....#..#....#│
        └──────────────────────────────────────────────────────────────┘
    """, border=True)
    assert sec == 10612
