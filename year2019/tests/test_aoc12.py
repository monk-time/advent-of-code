from inspect import cleandoc

from year2019.aoc12 import find_loop, solve, total_energy, execute_time_step, parse

sample1 = cleandoc("""
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
""")

sample2 = cleandoc("""
    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>
""")


def test_total_energy():
    planets = list(parse(sample1))
    for _ in range(10):
        execute_time_step(planets)
    assert total_energy(planets) == 179

    planets = list(parse(sample2))
    for _ in range(100):
        execute_time_step(planets)
    assert total_energy(planets) == 1940


def test_find_loop():
    planets = list(parse(sample1))
    assert find_loop(planets) == 2772


def test_solve():
    assert solve() == (12082, 295693702908636)
