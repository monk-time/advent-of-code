'use strict';

{
    const digits = [...document.body.textContent.trim()].map(Number);
    const sumMatching = shift => digits
        .filter((n, i, a) => n === a[shift(i, a.length) % a.length])
        .reduce((sum, n) => sum + n, 0);
    console.log([i => i + 1, (i, len) => i + len / 2].map(sumMatching));
}

// Another solution with a dynamically built regex
{
    const s = document.body.textContent.trim();
    const sumMatching = (ss, re) => (ss.match(new RegExp(re, 'g')) || [])
        .reduce((sum, c) => sum + +c, 0);
    console.log(sumMatching(s + s[0], '(\\d)(?=\\1)'));
    console.log(sumMatching(s + s.slice(0, s.length / 2), `(\\d)(?=.{${s.length / 2 - 1}}\\1)`));
}
