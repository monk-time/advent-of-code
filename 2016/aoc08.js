'use strict';

{
    const getGrid = (n, m) => [...new Array(m)].map(() => new Array(n).fill(0)),
        on = n => a => Array(n).fill(1).concat(a.slice(n)),
        shift = d => a => a.slice(-(d % a.length)).concat(a.slice(0, -(d % a.length))),
        replace = (i, el, a) => [...a.slice(0, i), el, ...a.slice(i + 1)],
        replaceCol = (j, col, grid) => grid.map((a, i) => replace(j, col[i], a));
    const op = {
        rect: (n, m) => grid => grid.slice(0, m).map(on(n)).concat(grid.slice(m)),
        rotate: {
            row:    (i, d) => grid =>    replace(i, shift(d)(grid[i]), grid),
            column: (j, d) => grid => replaceCol(j, shift(d)(grid.map(a => a[j])), grid),
        }
    };
    const re = /([a-z]+) (?:([a-z]+) )?\D*(\d+)\D+(\d+)/,
        ops = s => (([, f, g, n, m]) => (g ? op[f][g] : op[f])(+n, +m))(s.match(re)),
        swipe = (s, grid0) => s.map(ops).reduce((grid, f) => f(grid), grid0),
        sum = a => a.reduce((n, el) => n + el, 0),
        sumAll = grid => sum(grid.map(sum)),
        input = document.body.textContent.trim().split('\n'),
        print = grid => grid.map(a => a.join('')).join('\n').replace(/0/g, ' ').replace(/1/g, '#');
    console.log(...[print, sumAll].map(f => f(swipe(input, getGrid(50, 6)))));
}
