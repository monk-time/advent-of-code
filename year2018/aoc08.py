from typing import List

from helpers import read_puzzle


def metadata(s: str) -> List[int]:
    nums = [int(n) for n in s.split()]
    index, res = 2, []
    stack = [nums[:index]]
    while stack:
        meta = stack[-1][1]  # can be overwritten later
        if stack[-1][0]:  # at the start of the next child
            num_children, meta = nums[index:index + 2]
            index += 2
            if num_children:
                stack.append([num_children, meta])
                continue  # skip the final handling of metadata entries
            else:
                stack[-1][0] -= 1
        else:
            stack.pop()
            if stack:  # handle cascading ends of nodes
                stack[-1][0] -= 1
        res += nums[index:index + meta]
        index += meta
    return res


if __name__ == '__main__':
    puzzle = read_puzzle()
    # puzzle = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    print(sum(metadata(puzzle)))
