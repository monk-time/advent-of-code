import re
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from helpers import read_puzzle

Edges = Dict[str, List[str]]


def parse(steps: str) -> Dict[str, Edges]:
    graph = {'out': defaultdict(list), 'in': defaultdict(list)}
    matches = (re.findall(r'\b[A-Z]\b', s) for s in steps.splitlines())
    for a, b in matches:
        graph['out'][a].append(b)
        graph['in'][b].append(a)
    return graph


def toposort(graph: Dict[str, Edges]) -> Iterable[str]:
    no_incoming_edges = [s for s in graph['out'].keys() if s not in graph['in'].keys()]
    while no_incoming_edges:
        no_incoming_edges.sort(reverse=True)
        visited = no_incoming_edges.pop()
        yield visited
        for v_next in graph['out'][visited]:
            graph['in'][v_next].remove(visited)
            if not graph['in'][v_next]:
                no_incoming_edges.append(v_next)


def work(steps: str, workers: int, delay: int) -> Tuple[str, int]:
    graph = parse(steps)
    available = [s for s in graph['out'].keys() if s not in graph['in'].keys()]
    # Store each job as a pair of the absolute time of its finish and a letter
    worker_queue: List[Tuple[int, str]] = []
    second, result = 0, ''
    while available or worker_queue:
        # Give out jobs to available workers
        available.sort()
        free_workers = workers - len(worker_queue)
        for step in available[:free_workers]:
            worker_queue.append((second + delay + ord(step) - 64, step))
        available = available[free_workers:]
        # Skip time straight to when the next step is finished
        worker_queue.sort()
        [(second, visited), *worker_queue] = worker_queue
        result += visited
        # Remove the finished job from the graph
        for step_next in graph['out'][visited]:
            graph['in'][step_next].remove(visited)
            if not graph['in'][step_next]:
                available.append(step_next)
    return result, second


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(work(puzzle, 1, 0)[0], work(puzzle, 5, 60)[1])
