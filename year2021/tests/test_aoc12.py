from inspect import cleandoc

import pytest

from year2021.aoc12 import count_all_paths, parse, solve

sample_1 = cleandoc("""
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
""")

sample_2 = cleandoc("""
    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc
""")

sample_3 = cleandoc("""
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
""")


@pytest.mark.parametrize(
    'sample, paths', ((sample_1, 10), (sample_2, 19), (sample_3, 226))
)
def test_count_all_paths(sample: str, paths: set[str]):
    assert count_all_paths(parse(sample)) == paths


@pytest.mark.parametrize(
    'sample, paths', ((sample_1, 36), (sample_2, 103), (sample_3, 3509))
)
def test_count_all_paths_with_return(sample: str, paths: set[str]):
    assert count_all_paths(parse(sample), allow_return=True) == paths


def test_solve():
    assert solve() == (4912, 150004)
