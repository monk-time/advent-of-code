# https://adventofcode.com/2021/day/16
# tags: #decoding #binary #expressions

from dataclasses import dataclass
from functools import reduce
from itertools import chain
from operator import eq, gt, lt, mul
from typing import TYPE_CHECKING, Literal, cast

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable

type Bit = Literal[0, 1]
type BinNum = tuple[Bit, ...]

LEN_VER = 3
LEN_ID = 3
LEN_GROUP = 5
LEN_HEX = 4
LEN_TYPES = (15, 11)


@dataclass(frozen=True, slots=True)
class _PacketBase:
    version: int
    type_id: int


@dataclass(frozen=True, slots=True)
class LiteralPacket(_PacketBase):
    value: int


@dataclass(frozen=True, slots=True)
class OperatorPacket(_PacketBase):
    subpackets: tuple[Packet, ...]


type Packet = LiteralPacket | OperatorPacket


def parse(s: str) -> BinNum:
    def char_to_bin(ch: str) -> Generator[Bit]:
        return (cast('Bit', int(x)) for x in f'{int(ch, 16):04b}')

    return cast('BinNum', tuple(chain(*(char_to_bin(ch) for ch in s))))


def binnum_to_int(n: BinNum, i: int, length: int) -> int:
    value = 0
    for j in range(length):
        value = value * 2 + n[i + j]
    return value


def decode_literal(bn: BinNum, i: int) -> tuple[int, int]:
    value = 0
    while True:
        value = value * 16 + binnum_to_int(bn, i + 1, LEN_GROUP - 1)
        if bn[i] == 0:
            return value, i + LEN_GROUP
        i += LEN_GROUP


def decode_subpackets(bn: BinNum, i: int) -> tuple[list[Packet], int]:
    len_type_id = bn[i]
    len_val = LEN_TYPES[len_type_id]
    n = binnum_to_int(bn, i + 1, len_val)
    i += len_val + 1
    packets = list[Packet]()
    if len_type_id == 0:
        i_end = i + n
        while i < i_end:
            packet, i = decode(bn, i)
            packets.append(packet)
    else:
        for _ in range(n):
            packet, i = decode(bn, i)
            packets.append(packet)
    return packets, i


def decode(bn: BinNum, i: int = 0) -> tuple[Packet, int]:
    version = binnum_to_int(bn, i, LEN_VER)
    type_id = binnum_to_int(bn, i + LEN_VER, LEN_ID)
    i += LEN_VER + LEN_ID
    if type_id == 4:
        value, i = decode_literal(bn, i)
        return LiteralPacket(version, type_id, value), i
    packets, i = decode_subpackets(bn, i)
    return OperatorPacket(version, type_id, tuple(packets)), i


def sum_versions(packet: Packet) -> int:
    match packet:
        case LiteralPacket(version=version):
            return version
        case OperatorPacket(version=version, subpackets=sp):
            return version + sum(sum_versions(p) for p in sp)


OPERATORS: dict[int, Callable[[Iterable[int]], int]] = {
    0: sum,
    1: lambda nums: reduce(mul, nums),
    2: min,
    3: max,
    5: lambda nums: int(gt(*nums)),
    6: lambda nums: int(lt(*nums)),
    7: lambda nums: int(eq(*nums)),
}


def calc(packet: Packet) -> int:
    match packet:
        case LiteralPacket(value=value):
            return value
        case OperatorPacket(type_id=type_id, subpackets=sp):
            return OPERATORS[type_id](map(calc, sp))


def solve() -> tuple[int, int]:
    packet = decode(parse(read_puzzle()))[0]
    return sum_versions(packet), calc(packet)


if __name__ == '__main__':
    print(solve())
