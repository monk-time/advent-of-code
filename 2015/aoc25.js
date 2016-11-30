'use strict';
let nth = (r, c) => (r + c - 2) * ( r + c - 1) / 2 + c;

function genCode(number) {
    let code = 20151125;
    while (--number) {
        code = (code * 252533) % 33554393;
    }
    
    return code;
}

let [row, column] = document.body.textContent.match(/\d+/g).map(s => +s);

console.log(genCode(nth(row, column)));
