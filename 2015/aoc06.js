'use strict';
function parse(line) {
    let a = line.split(/ (?!o)(?:through )?|,/);
    return [a[0], a.slice(1, 5).map(n => parseInt(n, 10))];
}

function gridMap(f, grid, x1, y1, x2, y2) { // mutates grid
    for (let x = x1; x <= x2; x++) {
        for (let y = y1; y <= y2; y++) {
            grid[x][y] = f(grid[x][y]);
        }
    }
}

function getActions(on, off, toggle) {
    return {
        'turn on':  gridMap.bind(null, on),
        'turn off': gridMap.bind(null, off),
        toggle:     gridMap.bind(null, toggle)
    };
}

let actions1 = getActions(() => 1, () => 0, x => 1 - x),
    actions2 = getActions(x => x + 1, x => Math.max(0, x - 1), x => x + 2),
    input = document.body.textContent.trim().split('\n');

let getGrid = n => new Array(n).fill().map(() => new Array(n).fill(0)),
    sum = (a, b) => a + b,
    countAll = grid => grid.map(arr => arr.reduce(sum)).reduce(sum),
    exec = (cfg, actions, grid) => {
        cfg.forEach(([fName, coords]) => actions[fName](grid, ...coords));
        return grid;
    };

let cfg = input.map(parse),
    solve = actions => countAll(exec(cfg, actions, getGrid(1000)));
console.log([actions1, actions2].map(solve));
