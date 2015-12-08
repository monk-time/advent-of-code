'use strict';
let input = document.body.textContent.trim().split('\n'),
    [esc, char] = [/\\(?:"|\\)/g, /\\x[0-9a-f]{2}/g],
    matches = (re, s) => (s.match(re) || []).length,
    diff1 = s => 2 +     matches(esc, s) + 3 * matches(char, s),
    diff2 = s => 4 + 2 * matches(esc, s) +     matches(char, s),
    countAll = (arr, f) => arr.map(f).reduce((a, b) => a + b);

console.log([diff1, diff2].map(f => countAll(input, f)));
