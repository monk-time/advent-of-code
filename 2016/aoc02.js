'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const keypads = [
        ['123', '456', '789'],
        ['  1  ', ' 234 ', '56789', ' ABC ', '  D  ']
    ];
    const delta = { U: [-1, 0], D: [1, 0], L: [0, -1], R: [0, 1] };
    const code = (keypad, instructions, key0)  => {
        const key = ([i, j]) => keypad[i][j],
            point = k => keypad.map((s, i) => [i, s.indexOf(k)]).find(p => p[1] > -1);
        const shift = (dir, p) => p.map(
            (n, i) => Math.min(Math.max(n + delta[dir][i], 0), keypad.length - 1));
        const validate = p => key(p) !== ' ' ? p : null,
            move = (dir, p) => validate(shift(dir, p)) || p,
            findBtn = (s, p0) => s.split('').reduce((p, dir) => move(dir, p), p0);

        return instructions.reduce(
            (c, s) => c + key(findBtn(s, point(c[c.length - 1]))), key0
        ).slice(1);
    };

    console.log(...keypads.map(k => code(k, input, '5')));
}
