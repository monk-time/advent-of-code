'use strict';
let inRange  = (dim, i, j) => i >= 0 && j >= 0 && i < dim && j < dim,
    isCorner = (dim, i, j) => (i === 0 || i === dim - 1) && (j === 0 || j === dim - 1),
    getSafe  = (arr, i, j) => inRange(arr.length, i, j) && arr[i][j],
    nbsDelta = [
        [-1, -1], [-1, 0], [-1, 1],
        [ 0, -1],          [ 0, 1],
        [ 1, -1], [ 1, 0], [ 1, 1]
    ],
    nbs = (i, j) => nbsDelta.map(([di, dj]) => [i + di, j + dj]),
    countTruthy = arr => arr.filter(x => x).length,
    countNbs = (arr, i, j, cornersOn) => {
        let isOn = ([x, y]) => (cornersOn && isCorner(arr.length, x, y)) || getSafe(arr, x, y);
        return countTruthy(nbs(i, j).map(isOn));
    };

function update(grid, cornersOn = false) {
    let gridNew = grid.map(row => row.slice()),
        dim = grid.length; // grid must be square
    for (let i = 0; i < dim; i++) {
        for (let j = 0; j < dim; j++) {
            let on = countNbs(grid, i, j, cornersOn);
            gridNew[i][j] = (cornersOn && isCorner(dim, i, j)) ||
                (grid[i][j] ? (on === 2 || on === 3) : on === 3);
        }
    }

    return gridNew;
}

let input = document.body.textContent.trim(),
    grid = input.split('\n').map(s => [...s].map(ch => ch === '#')),
    countAll = arr => arr.reduce((sum, row) => sum + countTruthy(row), 0),
    nSteps = (n, corners) => [...new Array(n)].reduce(x => update(x, corners), grid);

console.log(countAll(nSteps(100)), countAll(nSteps(100, true)));

