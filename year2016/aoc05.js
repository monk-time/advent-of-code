// https://adventofcode.com/2016/day/5

/* eslint-disable no-eval */
/* global md5 */

'use strict';

{
    const [input, cache] = [document.querySelector('.puzzle-input').textContent, []];
    const getHash = n => md5(input + n);
    const hashesWith5Zeroes = function* () {
        yield* cache.map(getHash);
        let i = cache.length ? cache[cache.length - 1] : -1;
        while (true) {
            const hash = getHash(++i);
            if (hash.startsWith('00000')) {
                cache.push(i);
                yield hash;
            }
        }
    };

    const updateList = (arr, pos, val) => arr.map((x, i) => (i === pos ? val : x));
    const algs = [
        (pass, hash) => updateList(pass, pass.indexOf(undefined), hash[5]),
        (pass, hash) => {
            const pos = +hash[5]; // NaN if in a..e
            return pos < 8 && pass[pos] === undefined ?
                updateList(pass, pos, hash[6]) : pass;
        },
    ];

    const password = alg => {
        let pass = [...new Array(8)];
        for (const hash of hashesWith5Zeroes()) {
            pass = alg(pass, hash);
            if (!pass.includes(undefined)) break;
        }

        return pass.join('');
    };

    const main = () => console.log(...algs.map(password)); // 48 sec
    fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
        .then(r => r.text()).then(eval).then(main);
}
