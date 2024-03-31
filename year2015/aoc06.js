// https://adventofcode.com/2015/day/6

'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const parse = line => line.match(/(?:turn )?(\w+) (\d+),(\d+)\D+(\d+),(\d+)/);
    const cfg = input.map(parse).map(([, op, ...coords]) => [op, coords.map(Number)]);
    const getGrid = n => [...new Array(n)].map(() => new Array(n).fill(0));
    const sum = (a, b) => a + b;
    const sumGrid = grid => grid.map(arr => arr.reduce(sum)).reduce(sum);
    const mapGrid = (grid, f, [x1, y1, x2, y2]) => { // mutates grid
        for (let x = x1; x <= x2; x++) {
            for (let y = y1; y <= y2; y++) {
                grid[x][y] = f(grid[x][y]);
            }
        }

        return grid;
    };

    const exec = (ops, grid) =>
        cfg.reduce((acc, [op, coords]) => mapGrid(acc, ops[op], coords), grid);
    const solve = ops => sumGrid(exec(ops, getGrid(1000)));
    const ops1 = { on: () => 1, off: () => 0, toggle: l => 1 - l };
    const ops2 = { on: l => l + 1, off: l => Math.max(0, l - 1), toggle: l => l + 2 };
    console.log([ops1, ops2].map(solve));
}
