'use strict';

{
    const parse = input => {
        const grid = input.split('\n').map(s => ['.', ...s, '.'].map(ch => ch === '#'));
        const emptyRow = () => [...new Array(grid.length + 2)].fill(false);
        return [emptyRow(), ...grid, emptyRow()];
    };

    const sumMap = f => arr => arr.reduce((sum, x) => sum + f(x), 0);
    const sumMapAll = sumMap(sumMap(x => x));
    const nbs = (i, j) => [
        [i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
        [i,     j - 1],             [i,     j + 1],
        [i + 1, j - 1], [i + 1, j], [i + 1, j + 1],
    ];

    const update = (cornersOn = false) => grid => {
        const gridNew = grid.map(row => row.slice());
        const maxI = grid.length - 2; // grid must be square
        const onEdge = x => x === 1 || x === maxI;
        const isOn = ([x, y]) => grid[x][y] || cornersOn && onEdge(x) && onEdge(y);
        for (let i = 1; i <= maxI; i++) {
            for (let j = 1; j <= maxI; j++) {
                const on = sumMap(isOn)(nbs(i, j));
                gridNew[i][j] = on === 3 || on === 2 && grid[i][j] ||
                    cornersOn && onEdge(i) && onEdge(j);
            }
        }

        return gridNew;
    };

    const grid = parse(document.body.textContent.trim());
    const nSteps = (n, cornersOn) => [...new Array(n)].reduce(update(cornersOn), grid);
    console.log([false, true].map(b => sumMapAll(nSteps(100, b))));
}
