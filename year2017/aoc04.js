// https://adventofcode.com/2017/day/4

'use strict';

{
    const phrases = document.body.textContent.trim().split('\n');
    const noRepeats = (w, _, ws) => ws.filter(v => v === w).length === 1;
    const sortLetters = w => [...w].sort().join('');
    const isValid = f => ph => ph.split(' ').map(f).every(noRepeats);
    const count = f => phrases.filter(isValid(f)).length;

    console.log([w => w, sortLetters].map(count));
}
