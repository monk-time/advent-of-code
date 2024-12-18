import inspect
import os
import re
import timeit
from pathlib import Path


def read_puzzle(
    number: int | None = None, year: int | None = 2018, stripchars=None
) -> str:
    """Read the contents of the input file for the current puzzle.

    The number of the puzzle is determined by the filename of the caller,
    or can be specified explicitly.

    Raises:
        FileNotFoundError: if cannot find the puzzle file
    """
    if number:
        year_dir = Path(f'year{year}')
    else:
        caller_path: Path = Path(inspect.stack()[1].filename)
        caller: str = caller_path.stem.replace('test_', '')
        match = re.search(r'\d+', caller)
        if not match:
            msg = (
                'Cannot find the relevant puzzle input file. '
                'Make sure this function is called from a file '
                'with a puzzle number in the filename.'
            )
            raise FileNotFoundError(msg)
        number = int(match.group())
        year_dir = next(
            parent for parent in caller_path.parents if 'year' in parent.stem
        )
    puzzle_input = year_dir / 'inputs' / f'aoc{number:02d}.txt'
    return puzzle_input.read_text(encoding='utf-8').strip(stripchars)


def timed(f):
    """Decorate a function to measure its execution time.

    Use as a wrapper for recursive functions.
    """

    def inner(*args, **kwargs):
        start = timeit.default_timer()
        result = f(*args, **kwargs)
        total = timeit.default_timer() - start
        # Recreate function call string
        args_str = ', '.join(map(repr, args))
        kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
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


def border_wrap(lines: list[str]) -> list[str]:
    """Draw a border around an equally sized set of lines."""
    n = len(lines[0])
    return [
        f'┌{"─" * n}┐',
        *(f'│{"".join(s)}│' for s in lines),
        f'└{"─" * n}┘',
    ]


def fetch_inputs(year: int) -> None:
    import requests

    for day in range(25, 26):
        r = requests.get(
            f'https://adventofcode.com/{year}/day/{day}/input',
            cookies={'session': os.environ['SESSION']},
        )
        path = Path('inputs') / f'aoc{day:0>2}.txt'
        path.touch()
        path.write_text(r.text, encoding='utf-8', newline='\n')
        print(f'Downloaded input file for day #{day}')


if __name__ == '__main__':
    fetch_inputs(2020)
