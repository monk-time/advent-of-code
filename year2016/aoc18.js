// https://adventofcode.com/2016/day/18

'use strict';

{
    const nextRow = row => row.map((_, i) => {
        const left  = i > 0              && row[i - 1];
        const right = i < row.length - 1 && row[i + 1];
        return left !== right;
    });
    const safe = row => row.reduce((n, tile) => n + (tile ? 0 : 1), 0);
    const safeRows = (row, size) => {
        let n = safe(row);
        while (--size) {
            row = nextRow(row);
            n += safe(row);
        }

        return n;
    };

    const row = [...document.body.textContent.trim()].map(ch => ch === '^'); // true === traps
    console.log(...[40, 400000].map(n => safeRows(row, n)));
}
