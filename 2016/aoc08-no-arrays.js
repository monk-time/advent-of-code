'use strict';
// inspired by: https://github.com/fhaust/AoC2016/blob/master/Day8.hs

{
    const [w, h] = [50, 6],
        off = () => false,
        rect   = (n, m) => f => (x, y) => x < n && y < m || f(x, y),
        rotRow = (j, d) => f => (x, y) => f(y === j ? ((x - d) % w + w) % w : x, y),
        rotCol = (i, d) => f => (x, y) => f(x, x === i ? ((y - d) % h + h) % h : y),
        op = { rect, rotate: { row: rotRow, column: rotCol } },
        re = /([a-z]+) (?:([a-z]+) )?\D*(\d+)\D+(\d+)/,
        ops = s => (([, f, g, n, m]) => (g ? op[f][g] : op[f])(+n, +m))(s.match(re)),
        pixel = s => s.map(ops).reduce((prev, next) => next(prev), off),
        screen = f => [...new Array(h)].map((_, y) => [...new Array(w)].map((_, x) => f(x, y))),
        sum = a => a.reduce((n, el) => n + el, 0),
        sumAll = grid => sum(grid.map(sum)),
        print = grid => grid.map(a => a.map(b => b ? '#' : ' ').join('')).join('\n'),
        input = document.body.textContent.trim().split('\n');

    console.log(...[print, sumAll].map(f => f(screen(pixel(input)))));
}
