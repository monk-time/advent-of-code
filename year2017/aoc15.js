// https://adventofcode.com/2017/day/15

/* eslint-disable no-bitwise, no-constant-condition */

'use strict';

{
    const [d1, d2] = [2 ** 31 - 1, 2 ** 16 - 1];
    const gen = (factor, mul) => n => {
        while (true) {
            n = (n * factor) % d1;
            if (n % mul === 0) return n;
        }
    };

    const judgeCount = (a0, b0, facA, facB) => ([tries, mulA, mulB]) => {
        const [genA, genB] = [gen(facA, mulA), gen(facB, mulB)];
        let [a, b, i, counter] = [a0, b0, 0, 0];
        while (++i <= tries) {
            [a, b] = [genA(a), genB(b)];
            if ((a & d2) === (b & d2)) counter++;
        }

        return counter;
    };

    const [a, b] = document.body.textContent.match(/\d+/g).map(Number);
    const final = judgeCount(a, b, 16807, 48271);
    console.log([[40000000, 1, 1], [5000000, 4, 8]].map(final));
}
