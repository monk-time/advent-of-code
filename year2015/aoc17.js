// https://adventofcode.com/2015/day/17

'use strict';

{
    // pickSum(5, [1, 1, 2, 3, 4]) -> [4, 1], [4, 1], [3, 2], [3, 1, 1]
    const pickSum = function* (sum, items) {
        if (sum === 0) {
            yield [];
        } else if (items.length > 1) {
            const pick = items.pop();
            if (pick <= sum) {
                for (const rest of pickSum(sum - pick, items)) {
                    yield [pick, ...rest]; // all comb. with pick
                }
            }

            yield* pickSum(sum, items); // all comb. w/o pick
            items.push(pick);
        } else if (items[0] === sum) {
            yield [sum];
        }
    };

    const input = document.body.textContent.trim().split('\n').map(Number);
    const asc = (a, b) => a - b;
    const ways = [...pickSum(150, input.sort(asc))];
    const containers = ways.map(arr => arr.length).sort(asc);
    const minNum = containers[0];

    console.log(ways.length, containers.lastIndexOf(minNum) + 1);
}
