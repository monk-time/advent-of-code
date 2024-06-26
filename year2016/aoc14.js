// https://adventofcode.com/2016/day/14

/* eslint-disable no-eval */
/* global md5 */

'use strict';

{
    const keys = (salt, hasher, nth = 64) => {
        const cache = [];
        let [foundKeys, i3, countNext1k, five] = [0, 0, 0, null];
        for (let i = 0; foundKeys < nth; i++) {
            if (!cache[i]) {
                cache[i] = hasher(salt + i);
            }

            if (!five) {
                const m = cache[i].match(/(.)\1\1/);
                if (m) {
                    five = m[1][0].repeat(5);
                    i3 = i;
                }
            } else if (countNext1k++ < 1000) {
                if (cache[i].includes(five)) {
                    foundKeys++;
                    [i, countNext1k, five] = [i3, 0, null]; // rewind
                }
            } else {
                [i, countNext1k, five] = [i3, 0, null];
            }
        }

        return i3;
    };

    const md5Stretched = (hash, times = 2016) => {
        while (times--) hash = md5(hash);
        return md5(hash);
    };

    const input = document.querySelector('.puzzle-input').textContent;
    const main = () => console.log([md5, md5Stretched].map(f => keys(input, f))); // 64 sec
    fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
        .then(r => r.text()).then(eval).then(main);
}
