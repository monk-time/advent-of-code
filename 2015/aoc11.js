// 7.5 sec :(
/* eslint-disable no-multi-spaces */

'use strict';

{
    const abc    = 'abcdefghijklmnopqrstuvwxyz';
    const base26 = '0123456789abcdefghijklmnop';
    const badChars = ['i', 'o', 'l'];
    const shift   = ch => base26[abc.indexOf(ch)];        // 'a' -> '0'
    const unshift = ch => abc[base26.indexOf(ch)];        // '0' -> 'a'
    const toBase26 = s => [...s].map(shift).join('');     // 'abcxyz' -> '012nop'
    const toABC    = s => [...s].map(unshift).join('');   // '012nop' -> 'abcxyz'
    const padA = (s, n) => ('a'.repeat(n) + s).slice(-n); // 'xyz' -> 'aaaaaxyz'
    const incPass = s => padA(toABC((parseInt(toBase26(s), 26) + 1).toString(26)), 8);

    const nextPassWithoutIOL = s => {
        s = incPass(s);
        const badCharsPos = badChars.map(ch => s.indexOf(ch)).filter(n => n !== -1);
        const firstBad = Math.min(...badCharsPos);
        if (firstBad < Infinity) {
            const nextChar = abc[(abc.indexOf(s[firstBad]) + 1) % 26];
            return s.slice(0, firstBad) + nextChar + 'a'.repeat(s.length - firstBad - 1);
        }

        return s;
    };

    const isGoodPass = s => {
        let pairs = 0;
        let seq = 0;
        let skipNext = false;
        let prev = s[0];
        for (let i = 1; i < s.length; i++) {
            const ch = s[i];
            const diff = ch.charCodeAt() - prev.charCodeAt();
            if (pairs < 2) {
                if (skipNext) {
                    skipNext = false;
                } else if (diff === 0) {
                    pairs++;
                    skipNext = true;
                }
            }

            if (seq < 2) seq = diff === 1 ? seq + 1 : 0;
            if (pairs === 2 && seq === 2) return true;
            prev = ch;
        }

        return false;
    };

    const nextGoodPass = s => {
        let pass = nextPassWithoutIOL(s);
        while (!isGoodPass(pass)) {
            pass = nextPassWithoutIOL(pass);
        }

        return pass;
    };

    console.time('main');
    const input = document.querySelector('.puzzle-input').textContent;
    const part1 = nextGoodPass(input);
    console.log(part1, nextGoodPass(part1));
    console.timeEnd('main');
}
