import inspect
import os
import re
import timeit
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = [
    'border_wrap',
    'print_peak_memory_used',
    'read_puzzle',
    'timed',
]


def read_puzzle(
    number: int | None = None, year: int | None = 2018, *, strip: bool = True
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
    path = year_dir / 'inputs' / f'aoc{number:02d}.txt'
    input_text = path.read_text(encoding='utf-8')
    return input_text.strip() if strip else input_text


def timed[**P, T](f: Callable[P, T]) -> Callable[P, T]:
    """Decorate a function to measure its execution time.

    Use as a wrapper for recursive functions.
    """

    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
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

    for day in range(1, 26):
        r = requests.get(
            f'https://adventofcode.com/{year}/day/{day}/input',
            cookies={'session': os.environ['SESSION']},
        )
        path = Path(f'year{year}/inputs') / f'aoc{day:0>2}.txt'
        path.touch()
        path.write_text(r.text, encoding='utf-8', newline='\n')
        print(f'Downloaded input file for day #{day}')
        sleep(1)


if __name__ == '__main__':
    fetch_inputs(2022)
