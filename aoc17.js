'use strict';
function* combineN(total, items) {
    if (total === 0) {
        yield [];
    } else if (items.length > 1) {
        let pick = items.pop();
        if (pick <= total) {
            for (let rest of combineN(total - pick, items)) {
                yield [pick, ...rest]; // all comb. with pick
            }
        }

        yield* combineN(total, items); // all comb. w/o pick
        items.push(pick);
    } else if (items[0] === total) {
        yield [total];
    }
}

let input = document.body.textContent.trim().split('\n').map(s => +s),
    asc = (a, b) => a - b,
    ways = [...combineN(150, input.sort(asc))],
    containers = ways.map(arr => arr.length).sort(asc),
    minNum = containers[0];

console.log(ways.length, containers.lastIndexOf(minNum) + 1);
