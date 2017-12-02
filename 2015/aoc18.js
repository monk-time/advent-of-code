'use strict';

{
    const parse = input => {
        const grid = input.split('\n').map(s => ['.', ...s, '.'].map(ch => ch === '#'));
        const emptyRow = () => [...new Array(grid.length + 2)].fill(false);
        return [emptyRow(), ...grid, emptyRow()];
    };

    const countTruthy = arr => arr.filter(x => x).length;
    const nbs = (i, j) => [
        [i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
        [i,     j - 1],             [i,     j + 1],
        [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]
    ];

    const update = (grid, cornersOn = false) => {
        const gridNew = grid.map(row => row.slice());
        const maxI = grid.length - 2; // grid must be square
        const isOn = ([x, y]) => cornersOn && (x === 1 || x === maxI) && (y === 1 || y === maxI) || grid[x][y];
        for (let i = 1; i <= maxI; i++) {
            for (let j = 1; j <= maxI; j++) {
                const on = countTruthy(nbs(i, j).map(isOn));
                gridNew[i][j] = cornersOn && (i === 1 || i === maxI) && (j === 1 || j === maxI) ||
                    (grid[i][j] ? on === 2 || on === 3 : on === 3);
            }
        }

        return gridNew;
    };

    const grid = parse(document.body.textContent.trim());
    const nSteps = (n, corners) => [...new Array(n)].reduce(x => update(x, corners), grid);
    const countAll = arr => arr.reduce((sum, row) => sum + countTruthy(row), 0);

    console.log(countAll(nSteps(100)), countAll(nSteps(100, true)));
}
