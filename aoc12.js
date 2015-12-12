'use strict';
let input = JSON.parse(document.body.textContent),
    vals = obj => Object.keys(obj).map(k => obj[k]);

function sumNumbers(obj, part2 = false) {
    if (obj instanceof Object) {
        let rec = !part2 || obj instanceof Array || vals(obj).indexOf('red') === -1;
        return rec ? vals(obj).reduce((sum, v) => sum + sumNumbers(v, part2), 0) : 0;
    } else {
        return Number.isInteger(obj) ? obj : 0;
    }
}

console.log(sumNumbers(input), sumNumbers(input, true));
