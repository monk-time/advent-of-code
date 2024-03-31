// https://adventofcode.com/2017/day/19

'use strict';

{
    const input = document.body.textContent.split('\n');
    const maze = ([i, j]) => input[i][j];
    const deltas = { down: [1, 0], right: [0, 1], up: [-1, 0], left: [0, -1] };
    const move = ([i, j], [di, dj]) => [i + di, j + dj];
    const isALetter = ij => !' +|-'.includes(maze(ij));
    const endOfLine = ij => ' +'.includes(maze(ij));
    const turn = d => (d[0] === 0 ? [deltas.down, deltas.up] : [deltas.left, deltas.right]);
    const legalTurn = (d, ij) => turn(d).find(dNew => maze(move(ij, dNew)) !== ' ');

    let ij = [0, input[0].indexOf('|')];
    let [d, res, steps] = [deltas.down, '', 0];
    while (d) {
        do {
            ij = move(ij, d);
            steps++;
            if (isALetter(ij)) res += maze(ij);
        } while (!endOfLine(ij));

        d = legalTurn(d, ij);
    }

    console.log([res, steps]);
}
