'use strict';
function parse(input) {
    let grid = input.split('\n').map(s => ['.', ...s, '.'].map(ch => ch === '#')),
        dim = grid.length,
        emptyRow = dim => [...new Array(dim + 2)].fill(0);
    return [emptyRow(dim), ...grid, emptyRow(dim)];
}

let isCorner = (dim, i, j) => (i === 1 || i === dim - 2) && (j === 1 || j === dim - 2),
    nbsDelta = [
        [-1, -1], [-1, 0], [-1, 1],
        [ 0, -1],          [ 0, 1],
        [ 1, -1], [ 1, 0], [ 1, 1]
    ],
    nbs = (i, j) => nbsDelta.map(([di, dj]) => [i + di, j + dj]),
    countTruthy = arr => arr.filter(x => x).length;

function update(grid, cornersOn = false) {
    let gridNew = grid.map(row => row.slice()),
        dim = grid.length, // grid must be square
        isOn = ([x, y]) => cornersOn && isCorner(dim, x, y) || grid[x][y];
    for (let i = 1; i < dim - 1; i++) {
        for (let j = 1; j < dim - 1; j++) {
            let on = countTruthy(nbs(i, j).map(isOn));
            gridNew[i][j] = cornersOn && isCorner(dim, i, j) ||
                (grid[i][j] ? on === 2 || on === 3 : on === 3);
        }
    }

    return gridNew;
}

let grid = parse(document.body.textContent.trim()),
    nSteps = (n, corners) => [...new Array(n)].reduce(x => update(x, corners), grid),
    countAll = arr => arr.reduce((sum, row) => sum + countTruthy(row), 0);

console.log(countAll(nSteps(10)), countAll(nSteps(10, true)));
