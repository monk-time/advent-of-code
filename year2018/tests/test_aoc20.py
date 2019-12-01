from inspect import cleandoc

import pytest

from aoc20 import map_to_str, max_doors_in_shortest_path, parse_map, solve


def test_parse_map():
    m = parse_map('^ENWWW$')
    assert m[(0, -1)] == '#'
    assert m[(0, 0)] == 'X'
    assert m[(0, 1)] == '|'
    assert m[(0, 2)] == '.'


samples = (
    ('^WNE$', cleandoc("""
        #####
        #.|.#
        #-###
        #.|X#
        #####
    """)),
    ('^ENWWW$', cleandoc("""
        #########
        #.|.|.|.#
        #######-#
            #X|.#
            #####
    """)),
    ('^ENWWW(NEEE|SSE(EE|N))$', cleandoc("""
        #########
        #.|.|.|.#
        #-#######
        #.|.|.|.#
        #-#####-#
        #.#.#X|.#
        #-#-#####
        #.|.|.|.#
        #########
    """)),
    ('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', cleandoc("""
        ###########
        #.|.#.|.#.#
        #-###-#-#-#
        #.|.|.#.#.#
        #-#####-#-#
        #.#.#X|.#.#
        #-#-#####-#
        #.#.|.|.|.#
        #-###-###-#
        #.|.|.#.|.#
        ###########
    """)),
    ('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', cleandoc("""
        #############
        #.|.|.|.|.|.#
        #-#####-###-#
        #.#.|.#.#.#.#
        #-#-###-#-#-#
        #.#.#.|.#.|.#
        #-#-#-#####-#
        #.#.#.#X|.#.#
        #-#-#-###-#-#
        #.|.#.|.#.#.#
        ###-#-###-#-#
        #.|.#.|.|.#.#
        #############
    """)),
    ('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$',
     cleandoc("""
        ###############
        #.|.|.|.#.|.|.#
        #-###-###-#-#-#
        #.|.#.|.|.#.#.#
        #-#########-#-#
        #.#.|.|.|.|.#.#
        #-#-#########-#
        #.#.#.|X#.|.#.#
        ###-#-###-#-#-#
        #.|.#.#.|.#.|.#
        #-###-#####-###
        #.|.#.|.|.#.#.#
        #-#-#####-#-#-#
        #.#.|.|.|.#.|.#
        ###############
    """)),
)


@pytest.mark.parametrize("puzzle, map_str", samples)
def test_map_to_str(puzzle, map_str):
    assert map_to_str(parse_map(puzzle)) == map_str


sample_n_doors = (3, 5, 10, 18, 23, 31)
part1 = ((pzl, (n, 0)) for (pzl, _), n in zip(samples, sample_n_doors))


@pytest.mark.parametrize("puzzle, n_doors", part1)
def test_max_doors_in_shortest_path(puzzle, n_doors):
    assert max_doors_in_shortest_path(parse_map(puzzle)) == n_doors


def test_solve():
    assert solve() == (3930, 8240)
