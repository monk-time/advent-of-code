/* eslint-disable no-bitwise */

'use strict';

{
    // Each char in crc corresponds to (max power of 2 dividing n) symbols of data;
    // it's equal to '1' if such a chunk has an even amount of 1
    const popcount = a => a.reduce((n, c) => n + c);
    const checksum = (s, len) => {
        const [a, chunkSize] = [[...s].map(Number), len & -len];
        let [pos, crc]  = [0, ''];
        while (a.length < len) {
            a.push(0);
            for (let i = a.length - 2; i >= 0; i--) { // skip 0 added above
                a.push(1 - a[i]);
            }

            while (a.length >= pos + chunkSize) {
                const chunk = a.slice(pos, pos + chunkSize);
                crc += String(1 - (popcount(chunk) % 2));
                pos += chunkSize;
            }
        }

        return crc;
    };

    const input = document.querySelector('.puzzle-input').textContent;
    console.log([272, 35651584].map(n => checksum(input, n)));
}
