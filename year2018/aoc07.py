# https://adventofcode.com/2018/day/7

import re
from collections import defaultdict

from utils_proxy import read_puzzle

type Graph = dict[str, defaultdict[str, list[str]]]


def parse(steps: str) -> Graph:
    graph: Graph = {'out': defaultdict(list), 'in': defaultdict(list)}
    for s in steps.splitlines():
        a, b = re.findall(r'\b[A-Z]\b', s)
        graph['out'][a].append(b)
        graph['in'][b].append(a)
    return graph


def work(steps: str, workers: int, delay: int) -> tuple[str, int]:
    g = parse(steps)
    todo = [s for s in g['out'] if s not in g['in']]
    # Store each job as a pair of the absolute time of its finish and a letter
    in_process: list[tuple[int, str]] = []
    result, time = '', 0
    while todo or in_process:
        # Give out jobs to available workers
        todo.sort()
        free_workers = workers - len(in_process)
        in_process.extend(
            (time + delay + ord(job) - 64, job) for job in todo[:free_workers]
        )
        todo = todo[free_workers:]
        # Skip time to when the next job is finished
        in_process.sort()
        [(time, finished), *in_process] = in_process
        result += finished
        # Remove the finished job from the graph and find new available jobs
        for next_job in g['out'][finished]:
            g['in'][next_job].remove(finished)
            if not g['in'][next_job]:
                todo.append(next_job)
    return result, time


def solve():
    puzzle = read_puzzle()
    return work(puzzle, 1, 0)[0], work(puzzle, 5, 60)[1]


if __name__ == '__main__':
    print(solve())
