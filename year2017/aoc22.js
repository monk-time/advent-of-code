// https://adventofcode.com/2017/day/22

'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const halfWidth = Math.floor(input[0].length / 2); // the input is guaranteed to be odd-sized
    const key = (i, j) => `${i},${j}`;
    const parseLine = (s, i) => [...s.trim()].map((c, j) =>
        [key(i - halfWidth, j - halfWidth), '.W#F'.indexOf(c)]);
    const nodes0 = [].concat(...input.map(parseLine))
        .reduce((acc, [ij, v]) => Object.assign(acc, { [ij]: v }), {});

    const dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]; // URDL
    const add = ([i, j], [di, dj]) => [i + di, j + dj];
    const steps = (n, jump, nodes, pos = [0, 0], dir = 0) => {
        nodes = { ...nodes };
        let infected = 0;
        for (let step = 0; step < n; step++) {
            const ij = key(...pos);
            const node = nodes[ij] || 0;
            [dir, nodes[ij]] = [(dir + (node - 1) + 4) % 4, (node + jump) % 4];
            if (nodes[ij] === 2) infected++;
            pos = add(pos, dirs[dir]);
        }

        return infected;
    };

    console.log(steps(10000, 2, nodes0), steps(10000000, 1, nodes0)); // 7 sec
}
