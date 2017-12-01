// Helpful reusable segments
/* eslint-disable */

/* Comment header
JavaScript (JS, ES6+), both parts in one, runs in the FF/Chrome browser console on the /input page (F12 → Console → paste → Enter):
*/

// MD5
fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
    .then(r => r.text()).then(eval).then(main);

// Inputs (from /input or the puzzle itself)
const input = document.body.textContent.trim();
const input2 = document.querySelector('.puzzle-input').textContent.trim();

// Generate nxn grid
const getGrid = n => new Array(n).fill().map(() => new Array(n).fill(0));
const getGrid2 = n => [...new Array(n)].map(() => new Array(n).fill(0));

// Timed execution
const timed = f => { console.time('main'); f(); console.timeEnd('main'); };

// Permutation generator
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
