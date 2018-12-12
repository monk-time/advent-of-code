import re

from helpers import read_puzzle, timed


@timed
def high_score(s: str) -> int:
    players, last_marble = map(int, re.findall(r'\d+', s))
    marble, index = 0, 0
    circle, scores = [marble], [0] * players
    # print(f'[{"-" * len(str(players))}] (0)')
    for marble in range(1, last_marble + 1):
        player = marble % players
        if marble % 23 != 0:
            index = ((index + 1) % len(circle)) + 1
            circle.insert(index, marble)
        else:
            index = (index - 7) % len(circle)
            scores[player] += marble + circle.pop(index)
        # print_state(players, last_marble, circle, player, index)
    return max(scores)


def print_state(players, last_marble, circle, player, index):
    pad_pl, pad_mrbl = len(str(players)), len(str(last_marble))
    marbles_str = ' '.join(f'{n:{pad_mrbl}d}' for n in circle)
    s = f'[{player or players:{pad_pl}d}] {marbles_str} '
    i = 2 + pad_pl + index * (pad_mrbl + 1)
    s2 = s[:i] + '(' + s[i + 1:i + 1 + pad_mrbl] + ')' + s[i + 2 + pad_mrbl:]
    assert len(s) == len(s2)
    # Move an opening brace closer to a number
    print(re.sub(r'\(( +)', r'\1(', s2))


if __name__ == '__main__':
    puzzle = read_puzzle()
    print(high_score(puzzle))
    # print(high_score(puzzle.replace(' points', '00 points')))
