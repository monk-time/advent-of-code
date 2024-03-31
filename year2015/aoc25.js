// https://adventofcode.com/2015/day/25

'use strict';

{
    const nth = (row, col) => (row + col - 2) * (row + col - 1) / 2 + col;
    const genCode = (n, code = 20151125) => {
        while (--n) code = (code * 252533) % 33554393;
        return code;
    };

    const [row, col] = document.body.textContent.match(/\d+/g).map(Number);
    console.log(genCode(nth(row, col)));
}
