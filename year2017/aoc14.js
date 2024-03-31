// https://adventofcode.com/2017/day/14

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
    // End of copy-paste from Day 10 (sorry, no imports in browser)

    const sum = arr => arr.reduce((x, y) => x + y);
    const hexToBin = h => parseInt(h, 16).toString(2).padStart(4, '0');
    const hexToBits = h => hexToBin(h).split('').map(Number);
    const bitRow = s => [].concat(...s.split('').map(hexToBits));

    const input = document.querySelector('.puzzle-input').textContent;
    const grid = [...new Array(128)].map((_, i) => bitRow(knotHash(`${input}-${i}`)));
    console.log(sum(grid.map(sum)));

    const eraseRegion = (i, j) => { // mutates grid
        const stack = [[i, j]];
        while (stack.length) {
            [i, j] = stack.pop();
            if (i < 0 || j < 0 || i >= grid.length || j >= grid.length) continue;
            if (grid[i][j] === 0) continue;
            grid[i][j] = 0;
            stack.push([i - 1, j], [i, j - 1], [i + 1, j], [i, j + 1]);
        }
    };

    let regions = 0;
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid.length; j++) {
            if (grid[i][j] === 0) continue;
            regions++;
            eraseRegion(i, j);
        }
    }

    console.log(regions);
}
