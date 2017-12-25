// Helpful reusable segments
/* eslint-disable no-unused-vars, no-eval, no-undef */

/* Comment header
**JavaScript (JS, ES6+)**, both parts in one, runs in the FF/Chrome
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

    // Generate and draw infinite grid from an odd-sized center segment
    const halfWidth = Math.floor(input[0].length / 2);
    const key = (i, j) => `${i},${j}`;
    const parseLine = (s, i) => [...s.trim()].map((c, j) =>
        [key(i - halfWidth, j - halfWidth), c]);
    const nodes0 = [].concat(...input.map(parseLine))
        .reduce((acc, [ij, v]) => Object.assign(acc, { [ij]: v }), {});

    const draw = (nodes, [i0, j0] = [0, 0], zero = '.') => {
        const entries = Object.entries(nodes).map(([k, v]) => [k.split(',').map(Number), v]);
        const xs = entries.map(([[i]]) => i);
        const ys = entries.map(([[, j]]) => j);
        const [xMin, xMax] = [Math.min(...xs), Math.max(...xs)];
        const [yMin, yMax] = [Math.min(...ys), Math.max(...ys)];
        const offset = Math.max(...[xMin, xMax, yMin, yMax, i0, j0].map(Math.abs));
        const a = [...new Array(2 * offset + 1)].map(() => []);
        for (let i = -offset; i <= offset; i++) {
            for (let j = -offset; j <= offset; j++) {
                const node = nodes[key(i, j)] || zero;
                a[i + offset][j + offset] = i === i0 && j === j0 ? `[${node}]` : ` ${node} `;
            }
        }

        return a.map(row => row.join('').replace(/\] | {2}| \[/g, s => s.trim() || ' ')).join('\n');
    };

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
