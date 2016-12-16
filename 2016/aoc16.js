'use strict';

{
    const input = document.querySelector('.puzzle-input').textContent;
    const data = (s, n) => {
        if (s.length >= n) return s.slice(0, n);
        return data(s + '0' + [...s].reverse().map(b => '10'[+b]).join(''), n);
    };
    const checksum = (s, n) => {
        // max power of 2 dividing n = how many symbols of data correspond to one in crc
        const chunkSize = n & -n;
        let [d, crc] = [data(s, n), ''];
        while (d.length) {
            let chunk = d.slice(0, chunkSize);
            d = d.slice(chunkSize);
            // add '1' if a chunk has an even amount of 1
            crc += (chunk.split('1').length - 1) % 2 === 0 ? '1' : '0';
        }
        return crc;
    };

    console.log(...[272, 35651584].map(n => checksum(input, n)));
}
