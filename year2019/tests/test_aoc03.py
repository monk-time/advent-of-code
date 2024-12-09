from year2019.aoc03 import (
    find_closest_intersection,
    find_min_intersection_by_steps,
    parse,
    solve,
    trace_wire,
)

example1 = 'R8,U5,L5,D3\nU7,R6,D4,L4'


def test_parse():
    assert parse(example1) == (
        [('R', 8), ('U', 5), ('L', 5), ('D', 3)],
        [('U', 7), ('R', 6), ('D', 4), ('L', 4)],
    )


def test_trace_wire():
    wire1, wire2 = parse('U2,R1,L3\nD3,U1')
    assert trace_wire(wire1) == {
        (0, 0): 0,
        (0, 1): 1,
        (0, 2): 2,
        (1, 2): 3,
        (-1, 2): 5,
        (-2, 2): 6,
    }
    assert trace_wire(wire2) == {(0, 0): 0, (0, -1): 1, (0, -2): 2, (0, -3): 3}


def test_find_closest_intersection():
    wire1, wire2 = parse(example1)
    assert find_closest_intersection(wire1, wire2) == 6


def test_find_min_intersection_by_steps():
    wire1, wire2 = parse(example1)
    assert find_min_intersection_by_steps(wire1, wire2) == 30
    wire1, wire2 = parse(
        'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83'
    )
    assert find_min_intersection_by_steps(wire1, wire2) == 610
    wire1, wire2 = parse(
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    )
    assert find_min_intersection_by_steps(wire1, wire2) == 410


def test_solve():
    assert solve() == (258, 12304)
