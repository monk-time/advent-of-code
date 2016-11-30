'use strict';
let input = document.body.textContent.trim().split('\n'),
    [esc, char] = [/\\(?:"|\\)/g, /\\x[0-9a-f]{2}/g],
    matches = (re, s) => (s.match(re) || []).length,
    clean = s => s.replace(esc, 'X'), // for edge cases like "\\xce"
    diff1 = s => 2 +     matches(esc, s) + 3 * matches(char, clean(s)),
    diff2 = s => 4 + 2 * matches(esc, s) +     matches(char, clean(s)),
    countAll = (f, arr) => arr.reduce((a, b) => a + f(b), 0);

console.log([diff1, diff2].map(f => countAll(f, input)));
