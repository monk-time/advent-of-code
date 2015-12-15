'use strict';
let sum = arr => arr.reduce((a, b) => a + b, 0);

// splitN(100, 3) === [[1, 1, 98], [1, 2, 97], ..., [97, 2, 1], [98, 1, 1]]
function* splitN(n, parts, res = []) {
    let partialSum = sum(res);
    for (let i = 1; i < n - partialSum - (parts - 1) + 1; i++) {
        let resNew = [...res, i];
        if (parts > 2) {
            yield* splitN(n, parts - 1, resNew);
        } else {
            resNew.push(n - partialSum - i);
            yield resNew;
        }
    }
}

function maxScore(ingrs, spoonNum, calValue) {
    let max = 0;
    for (let spoons of splitN(spoonNum, ingrs.length)) {
        let ingrsAll = ingrs.map((ingr, i) => ingr.map(prop => prop * spoons[i])),
            cal = ingrsAll.map(ingr => ingr.pop()); // mutates ingrsAll
        if (calValue) {
            if (calValue !== sum(cal)) {
                continue;
            }
        }

        let propSum = ingrsAll.reduce((a, b) => a.map((prop, i) => prop + b[i])),
            score = propSum.reduce((acc, prop) => acc * Math.max(prop, 0), 1);
        if (score > max) {
            max = score;
        }
    }

    return max;
}

let input = document.body.textContent.trim().split('\n'),
    ingrs = input.map(s => s.match(/-?\d+/g).map(n => +n));

console.log(maxScore(ingrs, 100), maxScore(ingrs, 100, 500));
