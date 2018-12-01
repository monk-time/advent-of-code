import inspect
import re
from pathlib import Path


def read_puzzle() -> str:
    """Read the contents of the input file for the current puzzle."""
    # The number of the puzzle is determined by the filename of the caller
    caller: str = Path(inspect.stack()[1].filename).stem.replace('test_', '')
    pzl_num = re.search(r'\d+', caller)
    if not pzl_num:
        raise FileNotFoundError('Cannot find the relevant puzzle input file. '
                                'Make sure this function is called from a file '
                                'with a puzzle number in the filename.')
    puzzle_input = Path(__file__).parent / 'inputs' / f'aoc{pzl_num.group()}.txt'
    return puzzle_input.read_text(encoding='utf-8').strip()
