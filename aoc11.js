// 7.5 sec :(
'use strict';
let abc    = 'abcdefghijklmnopqrstuvwxyz',
    base26 = '0123456789abcdefghijklmnop',
    badChars = ['i', 'o', 'l'],
    shift   = ch => base26[abc.indexOf(ch)],  // 'a' -> '0'
    unshift = ch => abc[base26.indexOf(ch)],  // '0' -> 'a'
    toBase26 = s => [...s].map(shift).join(''),    // 'abcxyz' -> '012nop'
    toABC    = s => [...s].map(unshift).join(''),  // '012nop' -> 'abcxyz'
    padA = (s, n) => ('a'.repeat(n) + s).slice(-n),  // 'xyz' -> 'aaaaaxyz'
    incPass = s => padA(toABC((parseInt(toBase26(s), 26) + 1).toString(26)), 8);

function nextPassWithoutIOL(s) {
    s = incPass(s);
    let badCharsPos = badChars.map(ch => s.indexOf(ch)).filter(n => n !== -1),
        firstBad = Math.min(...badCharsPos);
    if (firstBad < Infinity) {
        let nextChar = abc[(abc.indexOf(s[firstBad]) + 1) % 26];
        return s.slice(0, firstBad) + nextChar + 'a'.repeat(s.length - firstBad - 1);
    }

    return s;
}

function isGoodPass(s) {
    let pairs = 0,
        seq = 0,
        skipNext = false,
        prev = s[0];
    for (let i = 1; i < s.length; i++) {
        let ch = s[i],
            diff = ch.charCodeAt() - prev.charCodeAt();
        if (pairs < 2) {
            if (skipNext) {
                skipNext = false;
            } else if (diff === 0) {
                pairs++;
                skipNext = true;
            }
        }

        if (seq < 2) {
            seq = diff === 1 ? seq + 1 : 0;
        }

        if (pairs === 2 && seq === 2) {
            return true;
        }

        prev = ch;
    }

    return false;
}

function nextGoodPass(s) {
    let pass = nextPassWithoutIOL(s);
    while (!isGoodPass(pass)) {
        pass = nextPassWithoutIOL(pass);
    }

    return pass;
}

console.time('main');
let input = document.querySelector('.puzzle-input').textContent,
    part1 = nextGoodPass(input);
console.log(part1, nextGoodPass(part1));
console.timeEnd('main');
