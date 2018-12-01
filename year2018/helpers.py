import inspect
from pathlib import Path


def read_puzzle() -> str:
    """Read the contents of the input file for the current puzzle."""
    # The number of the puzzle is determined by the filename of the caller
    puzzle = inspect.stack()[1].filename
    puzzle_input = Path('inputs') / Path(puzzle).with_suffix('.txt').name
    return puzzle_input.read_text(encoding='utf-8').strip()
