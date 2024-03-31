// https://adventofcode.com/2017/day/10

'use strict';

{
    const halfTwist = (len, a, pos, skip) => {
        const a2 = [...a];
        for (let i = 0; i < len; i++) {
            a2[(i + pos) % size] = a[(pos + len - i - 1 + size) % size];
        }

        return [a2, (pos + len + skip) % size, skip + 1];
    };

    const newList = () => [...new Array(size).keys()];
    const lengths1 = s => s.split(',').map(Number);
    const lengths2 = s => [...[...s].map(c => c.charCodeAt()), 17, 31, 73, 47, 23];
    const oneRound = (lengths, a = newList(), pos = 0, skip = 0) =>
        lengths.reduce((state, len) => halfTwist(len, ...state), [a, pos, skip]);

    const sparseHash = (lengths, a = newList(), pos = 0, skip = 0) => {
        for (let i = 0; i < 64; i++) {
            [a, pos, skip] = oneRound(lengths, a, pos, skip);
        }

        return a;
    };

    const denseHash = sparse => [...new Array(16)].map((_, block) => sparse
        .slice(block * 16, (block + 1) * 16)
        .reduce((x, y) => x ^ y) // eslint-disable-line no-bitwise
        .toString(16).padStart(2, '0')).join('');

    const knotHash = s => denseHash(sparseHash(lengths2(s)));
    const size = 256;

    const input = document.body.textContent.trim();
    const [a] = oneRound(lengths1(input));
    console.log(a[0] * a[1], knotHash(input));
}
