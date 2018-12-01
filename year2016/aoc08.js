'use strict';

{
    const getGrid = (n, m) => [...new Array(m)].map(() => new Array(n).fill(0));
    const on = n => a => new Array(n).fill(1).concat(a.slice(n));
    const shift = d => a => a.slice(-(d % a.length)).concat(a.slice(0, -(d % a.length)));
    const replace = (i, el, a) => [...a.slice(0, i), el, ...a.slice(i + 1)];
    const replaceCol = (j, col, grid) => grid.map((a, i) => replace(j, col[i], a));
    const op = {
        rect: (n, m) => grid => grid.slice(0, m).map(on(n)).concat(grid.slice(m)),
        rotate: {
            row:    (i, d) => grid =>    replace(i, shift(d)(grid[i]), grid),
            column: (j, d) => grid => replaceCol(j, shift(d)(grid.map(a => a[j])), grid),
        },
    };
    const re = /([a-z]+) (?:([a-z]+) )?\D*(\d+)\D+(\d+)/;
    const ops = s => (([, f, g, n, m]) => (g ? op[f][g] : op[f])(+n, +m))(s.match(re));
    const swipe = (s, grid0) => s.map(ops).reduce((grid, f) => f(grid), grid0);
    const sum = a => a.reduce((n, el) => n + el, 0);
    const sumAll = grid => sum(grid.map(sum));
    const print = grid => grid.map(a => a.join('')).join('\n').replace(/0/g, ' ').replace(/1/g, '#');
    const input = document.body.textContent.trim().split('\n');
    console.log(...[sumAll, print].map(f => f(swipe(input, getGrid(50, 6)))));
}

{
    // Array-less alternative solution.
    // Inspired by: https://github.com/fhaust/AoC2016/blob/master/Day8.hs
    const [w, h] = [50, 6];
    const off = () => false;
    const rect   = (n, m) => f => (x, y) => x < n && y < m || f(x, y);
    const rotRow = (j, d) => f => (x, y) => f(y === j ? ((x - d) % w + w) % w : x, y);
    const rotCol = (i, d) => f => (x, y) => f(x, x === i ? ((y - d) % h + h) % h : y);
    const op = { rect, rotate: { row: rotRow, column: rotCol } };
    const re = /([a-z]+) (?:([a-z]+) )?\D*(\d+)\D+(\d+)/;
    const ops = s => (([, f, g, n, m]) => (g ? op[f][g] : op[f])(+n, +m))(s.match(re));
    const pixel = s => s.map(ops).reduce((prev, next) => next(prev), off);
    const screen = f => [...new Array(h)].map((_, y) => [...new Array(w)].map((__, x) => f(x, y)));
    const sum = a => a.reduce((n, el) => n + el, 0);
    const sumAll = grid => sum(grid.map(sum));
    const print = grid => grid.map(a => a.map(b => (b ? '#' : ' ')).join('')).join('\n');
    const input = document.body.textContent.trim().split('\n');

    console.log(...[sumAll, print].map(f => f(screen(pixel(input)))));
}
