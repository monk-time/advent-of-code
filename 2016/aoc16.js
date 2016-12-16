// JavaScript (JS, ES2015/ES6), both parts in one, runs in the FF/Chrome browser console on the /input page.
'use strict';

{
    const input = document.querySelector('.puzzle-input').textContent;
    const data = (s, n) => {
        if (s.length >= n) return s.slice(0, n);
        return data(s + '0' + [...s].reverse().map(b => '10'[+b]).join(''), n);
    };
    const checksum = s => {
        let crc = '';
        while (s.length % 2 === 0) {
            for (let i = 0; i < s.length; i += 2) {
                crc += s[i] === s[i + 1] ? '1' : '0';
            }
            [s, crc] = [crc, ''];
        }
        return s;
    };

    console.log(...[272, 35651584].map(n => checksum(data(input, n))));
}
