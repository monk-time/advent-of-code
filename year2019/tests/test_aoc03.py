from year2019.aoc03 import parse, trace_wire, find_closest_intersection

example1 = 'R8,U5,L5,D3\nU7,R6,D4,L4'


def test_parse():
    assert parse(example1) == \
           ([('R', 8), ('U', 5), ('L', 5), ('D', 3)],
            [('U', 7), ('R', 6), ('D', 4), ('L', 4)])


def test_trace_wire():
    wire1, wire2 = parse('U2,R1,L3\nD3,U1')
    assert trace_wire(wire1) == {(0, 0), (0, 1), (0, 2), (1, 2), (-1, 2), (-2, 2)}
    assert trace_wire(wire2) == {(0, 0), (0, -1), (0, -2), (0, -3)}


def test_find_closest_intersection():
    wire1, wire2 = parse(example1)
    assert find_closest_intersection(wire1, wire2) == 6
