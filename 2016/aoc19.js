'use strict';

{
    const input = +document.querySelector('.puzzle-input').textContent;
    const winnerElf = n => 1 + 2 * (n - Math.pow(2, Math.floor(Math.log2(n))));
    // credit: /u/adventofcode2016
    const winnerElf2 = n => {
        let i = 1;
        while (i * 3 < n) {
            i *= 3;
        }
        return n - i + Math.max(n - 2 * i, 0);
    };

    console.log(winnerElf(input), winnerElf2(input));
}
