from year2019.aoc09 import run_intcode, solve, parse


def test_run_intcode():
    input_ = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    program = parse(input_)
    assert list(run_intcode(parse(input_))) == program
    assert list(run_intcode(parse('1102,34915192,34915192,7,4,7,99,0'))) == [1219070632396864]
    assert list(run_intcode(parse('104,1125899906842624,99'))) == [1125899906842624]


def test_solve():
    assert solve() == (4288078517, 69256)
