'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const [esc, char] = [/\\(?:"|\\)/g, /\\x[0-9a-f]{2}/g];
    const nMatches = (re, s) => (s.match(re) || []).length;
    const clean = s => s.replace(esc, 'X'); // for edge cases like "\\xce"
    const diff1 = s => 2 + nMatches(esc, s) + 3 * nMatches(char, clean(s));
    const diff2 = s => 4 + 2 * nMatches(esc, s) + nMatches(char, clean(s));
    const countAll = (f, arr) => arr.reduce((a, b) => a + f(b), 0);

    console.log([diff1, diff2].map(f => countAll(f, input)));
}
