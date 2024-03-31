// https://adventofcode.com/2015/day/15

'use strict';

{
    const sum = arr => arr.reduce((a, b) => a + b, 0);

    // splitN(5, 2) -> [1, 4], [2, 3], [3, 2], [4, 1]
    const splitN = function* (n, parts, res = []) {
        const partialSum = sum(res);
        for (let i = 1; i < n - partialSum - (parts - 1) + 1; i++) {
            const resNew = [...res, i];
            if (parts > 2) {
                yield* splitN(n, parts - 1, resNew);
            } else {
                resNew.push(n - partialSum - i);
                yield resNew;
            }
        }
    };

    const maxScore = (ings, spoonNum, calValue) => {
        let max = 0;
        for (const spoons of splitN(spoonNum, ings.length)) {
            const ingsAll = ings.map((ing, i) => ing.map(p => p * spoons[i]));
            const cal = ingsAll.map(ing => ing.pop()); // mutates ingsAll
            if (calValue && calValue !== sum(cal)) continue;

            const propSum = ingsAll.reduce((a, b) => a.map((p, i) => p + b[i]));
            const score = propSum.reduce((acc, p) => acc * Math.max(p, 0), 1);
            if (score > max) max = score;
        }

        return max;
    };

    const input = document.body.textContent.trim().split('\n');
    const ings = input.map(s => s.match(/-?\d+/g).map(Number));

    console.log(maxScore(ings, 100), maxScore(ings, 100, 500));
}
