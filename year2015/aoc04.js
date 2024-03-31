// https://adventofcode.com/2015/day/4

// Using [emn178's js-md5 library](https://www.npmjs.com/package/js-md5).
// Average exec. time (i7-4710HQ): 1.9 sec in FF42 (Scratchpad), 2.1 sec in Chrome 47 (Snippets).
/* eslint-disable no-eval */
/* global md5 */

'use strict';

{
    const mine = secret => {
        let [n, hash] = [0, ''];
        for (const zeroes of [5, 6].map(zn => '0'.repeat(zn))) {
            while (!hash.startsWith(zeroes)) {
                hash = md5(secret + ++n);
            }

            console.log(`md5(${secret}${n}): ${hash}`);
        }
    };

    const solve = () => {
        const input = document.querySelector('.puzzle-input').textContent.trim();
        console.time('main');
        mine(input);
        console.timeEnd('main');
    };

    fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
        .then(r => r.text()).then(eval).then(solve);
}
