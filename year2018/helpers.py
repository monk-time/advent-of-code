import inspect
import re
from pathlib import Path
from typing import Optional


def read_puzzle(number: Optional[int] = None) -> str:
    """Read the contents of the input file for the current puzzle."""
    # The number of the puzzle is determined by the filename of the caller
    if number:
        year_dir = Path('year2018')
    else:
        caller: str = Path(inspect.stack()[1].filename).stem.replace('test_', '')
        match = re.search(r'\d+', caller)
        if not match:
            raise FileNotFoundError('Cannot find the relevant puzzle input file. '
                                    'Make sure this function is called from a file '
                                    'with a puzzle number in the filename.')
        number = int(match.group())
        year_dir = Path(__file__).parent
    puzzle_input = year_dir / 'inputs' / f'aoc{number:02d}.txt'
    return puzzle_input.read_text(encoding='utf-8').strip()
