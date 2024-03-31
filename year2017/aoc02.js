// https://adventofcode.com/2017/day/2

'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const rows = input.map(r => r.split('\t').map(Number).sort((x, y) => x - y));
    const diff = r => r[r.length - 1] - r[0];
    const quot = r => (([x, y]) => y / x)(r.filter(x => r.some(evenDiv(x))));
    const evenDiv = x => y => x !== y && (y % x === 0 || x % y === 0);

    console.log([diff, quot].map(f => rows.reduce((sum, r) => sum + f(r), 0)));
}
