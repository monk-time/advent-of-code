import inspect
import re
import timeit
from pathlib import Path
from typing import List, Optional


def read_puzzle(number: Optional[int] = None, stripchars=None) -> str:
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
    return puzzle_input.read_text(encoding='utf-8').strip(stripchars)


def timed(f):
    """Decorator for measuring function execution time.

    Use as a wrapper for recursive functions.
    """

    def inner(*args, **kwargs):
        start = timeit.default_timer()
        result = f(*args, **kwargs)
        total = timeit.default_timer() - start
        # Recreate function call string
        args_str = ', '.join(map(repr, args))
        kwargs_str = ', '.join(f'{k}={repr(v)}' for k, v in kwargs.items())
        # 'a, b' if both not '' else 'a' or 'b'
        args_str = ', '.join(filter(None, [args_str, kwargs_str]))
        dots = '...' if len(args_str) > 50 else ''
        print(f'{f.__name__}({args_str[:50] + dots}): {total:.4g} sec')
        return result

    return inner


def print_peak_memory_used():
    import psutil
    max_memory = round(psutil.Process().memory_info().peak_wset / 1024 / 1024)
    print(f'Peak memory used: {max_memory} MB')


def border_wrap(lines: List[str]) -> str:
    """Draw a border around an equally sized set of lines."""
    n = len(lines[0])
    upper = f'┌{"─" * n}┐'
    lower = f'└{"─" * n}┘'
    lines = (f'│{s}│' for s in lines)
    return '\n'.join((upper, *lines, lower))


def block_unwrap(box: str, *, border: bool) -> List[str]:
    """Restore the original set of lines by removing whitespace and the border."""
    if border:
        return [s.strip()[1:-1] for s in box.strip().split('\n')[1:-1]]
    else:
        return [s.strip() for s in box.strip().split('\n')]
