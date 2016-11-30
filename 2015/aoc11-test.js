'use strict';
let abc = 'abcdefghijklmnopqrstuvwxyz';

function threeConsec(s) {
    let range = [...new Array(s.length - 2).keys()],
        checkParts = range.map(n => abc.indexOf(s.slice(n, n + 3)) > -1);
    return checkParts.indexOf(true) > -1;
}

let twoPairs = s => /(?:([a-z])\1.*){2}/.test(s),
    isGoodPass = s => threeConsec(s) && twoPairs(s);

let randomPass = () => {
    let rndChar = () => abc[Math.floor(Math.random(26) * 26)];
    return [...new Array(8)].map(rndChar).join('');
};

function isGoodPassIter(s) {
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

// isGoodPass('abcdffaa')
let passes = [...new Array(1000000)].map(randomPass);

console.time('func');
let func = JSON.stringify(passes.filter(isGoodPass));
console.timeEnd('func');
console.time('iter');
let iter = JSON.stringify(passes.filter(isGoodPassIter));
console.timeEnd('iter');
console.log(func === iter);
