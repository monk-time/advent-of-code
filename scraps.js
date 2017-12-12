// Helpful reusable segments
/* eslint-disable no-unused-vars, no-eval, no-undef */

/* Comment header
JavaScript (JS, ES6+), both parts in one, runs in the FF/Chrome
browser console on the /input page (F12 → Console):
*/

'use strict';

{
    // MD5
    fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
        .then(r => r.text()).then(eval).then(main);

    // Inputs (from /input or the puzzle itself)
    const input = document.body.textContent.trim();
    const input2 = document.querySelector('.puzzle-input').textContent;

    // Generate nxn grid
    const getGrid = n => new Array(n).fill().map(() => new Array(n).fill(0));
    const getGrid2 = n => [...new Array(n)].map(() => new Array(n).fill(0));

    // Timed execution
    (f => { console.time('main'); f(); console.timeEnd('main'); })(() => { // eslint-disable-line
    });

    // Timed execution for Promises
    const timed = f => () => { console.time('main'); f(); console.timeEnd('main'); }; // eslint-disable-line

    // Permutation generator and minmax tracker (separate)
    const permute = function* (arr, used = []) {
        if (arr.length === 0) yield [...used];
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            yield* permute(arr, used);
            arr.splice(i, 0, el);
            used.pop();
        }
    };

    const getMinmax = (arr, f) => Array.from(permute(arr), f)
        .reduce(extend, [Infinity, 0]);

    // Permutation generator and minmax tracker (combined)
    const extend = ([min, max], n) => [Math.min(min, n), Math.max(max, n)];
    const minmaxPerm = (arr, f, minmax = [Infinity, 0], used = []) => {
        if (arr.length === 0) return extend(minmax, f([...used]));
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            minmax = minmaxPerm(arr, f, minmax, used);
            arr.splice(i, 0, el);
            used.pop();
        }

        return minmax;
    };

    // splitN(5, 2) -> [1, 4], [2, 3], [3, 2], [4, 1]
    const splitN = function* (n, parts, res = []) {
        const partialSum = res.reduce((a, b) => a + b, 0);
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
}
