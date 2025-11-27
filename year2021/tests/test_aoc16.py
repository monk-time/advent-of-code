import pytest

from year2021.aoc16 import (
    LiteralPacket,
    OperatorPacket,
    Packet,
    calc,
    decode,
    parse,
    solve,
    sum_versions,
)


def test_parse():
    bin_str = ''.join(map(str, parse('D2FE28')))
    assert bin_str == '110100101111111000101000'


@pytest.mark.parametrize(
    's, packet',
    (
        (
            'D2FE28',
            LiteralPacket(version=6, type_id=4, value=2021),
        ),
        (
            '38006F45291200',
            OperatorPacket(
                version=1,
                type_id=6,
                subpackets=(
                    LiteralPacket(version=6, type_id=4, value=10),
                    LiteralPacket(version=2, type_id=4, value=20),
                ),
            ),
        ),
        (
            'EE00D40C823060',
            OperatorPacket(
                version=7,
                type_id=3,
                subpackets=(
                    LiteralPacket(version=2, type_id=4, value=1),
                    LiteralPacket(version=4, type_id=4, value=2),
                    LiteralPacket(version=1, type_id=4, value=3),
                ),
            ),
        ),
    ),
)
def test_decode(s: str, packet: Packet):
    assert decode(parse(s))[0] == packet


@pytest.mark.parametrize(
    's, result',
    (
        ('8A004A801A8002F478', 16),
        ('620080001611562C8802118E34', 12),
        ('C0015000016115A2E0802F182340', 23),
        ('A0016C880162017C3686B18A3D4780', 31),
    ),
)
def test_sum_versions(s: str, result: int):
    assert sum_versions(decode(parse(s))[0]) == result


@pytest.mark.parametrize(
    's, result',
    (
        ('C200B40A82', 3),
        ('04005AC33890', 54),
        ('880086C3E88112', 7),
        ('CE00C43D881120', 9),
        ('D8005AC2A8F0', 1),
        ('F600BC2D8F', 0),
        ('9C005AC2F8F0', 0),
        ('9C0141080250320F1802104A08', 1),
    ),
)
def test_calc(s: str, result: int):
    assert calc(decode(parse(s))[0]) == result


def test_solve():
    assert solve() == (979, 277110354175)
