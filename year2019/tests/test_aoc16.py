from itertools import pairwise

import pytest

from year2019.aoc16 import (
    apply_n_phases,
    apply_phase_of_fft,
    get_patterns,
    parse,
    pattern,
    real_signal,
    solve,
)


@pytest.mark.parametrize(
    'times, expected',
    (
        (1, (1, 0, -1, 0, 1, 0, -1, 0)),
        (2, (0, 1, 1, 0, 0, -1, -1, 0)),
        (3, (0, 0, 1, 1, 1, 0, 0, 0)),
        (4, (0, 0, 0, 1, 1, 1, 1, 0)),
        (5, (0, 0, 0, 0, 1, 1, 1, 1)),
        (6, (0, 0, 0, 0, 0, 1, 1, 1)),
        (7, (0, 0, 0, 0, 0, 0, 1, 1)),
        (8, (0, 0, 0, 0, 0, 0, 0, 1)),
    ),
)
def test_pattern(times, expected):
    assert pattern(length=8, times=times) == expected


def test_apply_phase_of_fft():
    signals = (
        '12345678',
        '48226158',
        '34040438',
        '03415518',
        '01029498',
    )
    patterns = get_patterns(8)
    for signal, next_signal in pairwise(signals):
        assert parse(next_signal) == apply_phase_of_fft(
            parse(signal), patterns
        )


@pytest.mark.parametrize(
    'test_input, expected',
    (
        ('80871224585914546619083218645595', '24176176'),
        ('19617804207202209144916044189917', '73745418'),
        ('69317163492948606335995924319873', '52432133'),
    ),
)
def test_apply_n_phases(test_input, expected):
    assert apply_n_phases(parse(test_input), 100) == parse(expected)


@pytest.mark.parametrize(
    'test_input, expected',
    (
        ('03036732577212944063491565474664', '84462026'),
        ('02935109699940807407585447034323', '78725270'),
        ('03081770884921959731165446850517', '53553731'),
    ),
)
def test_real_signal(test_input, expected):
    assert real_signal(parse(test_input)) == parse(expected)


def test_solve():
    assert solve() == ('19944447', '81207421')
