/* eslint-disable no-multi-spaces */

'use strict';

{
    const abc = 'abcdefghijklmnopqrstuvwxyz';
    const shift    = c => abc.indexOf(c); // 'a' -> 0, 'z' -> 25
    const unshift  = n => abc[n];         // 0 -> 'a', 25 -> 'z'
    const toBase26 = s => [...s].map(shift);       // 'abcaaaaz' -> [0, 1, 2, 0, 0, 0, 0, 25]
    const toABC    = a => a.map(unshift).join(''); // [0, 1, 2, 0, 0, 0, 0, 25] -> 'abcaaaaz'
    const badChars26 = ['i', 'l', 'o'].map(shift);

    const nextGoodPass = s => {
        let a = incPass26(toBase26(s));
        while (!isGoodPass(a)) a = incPass26(a);
        return toABC(a);
    };

    const incPass26 = (a, i = a.length - 1) => { // mutates the array
        while ((a[i] === 25) && i >= 0) a[i--] = 0;
        if (i === -1) return a;
        a[i] += 1;
        if (!badChars26.includes(a[i])) return a;
        a[i] += 1; // jump past the bad char
        while (++i < a.length) a[i] = 0;
        return a;
    };

    const isGoodPass = ([prev, ...rest]) => {
        let [pairs, seq, prevPair] = [0, 0, null];
        for (const c of rest) {
            if (pairs < 2 && c === prev && c !== prevPair) {
                pairs++;
                prevPair = c;
            }

            if (seq < 2) seq = c - prev === 1 ? seq + 1 : 0;
            if (pairs === 2 && seq === 2) return true;
            prev = c;
        }

        return false;
    };

    const input = document.querySelector('.puzzle-input').textContent;
    const part1 = nextGoodPass(input);
    console.log(part1, nextGoodPass(part1));
}
