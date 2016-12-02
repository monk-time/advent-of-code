'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const keypads = [
        ['123', '456', '789'],
        ['  1  ', ' 234 ', '56789', ' ABC ', '  D  ']
    ];
    const code = (keypad, instructions, start)  => {
        const correctKey = (i, j) => keypad[i][j] !== ' ' ? [i, j] : null,
            move = (pred, f) => (i, j) => pred(i, j) && correctKey(...f(i, j)) || [i, j];
        const moves = {
            U: move((i, _) => i > 0,                    (i, j) => [i - 1, j]),
            D: move((i, _) => i < keypad.length - 1,    (i, j) => [i + 1, j]),
            L: move((_, j) => j > 0,                    (i, j) => [i, j - 1]),
            R: move((_, j) => j < keypad[0].length - 1, (i, j) => [i, j + 1])
        };
        const key = ([i, j]) => keypad[i][j],
            coords = ch => keypad.map((s, i) => [i, s.indexOf(ch)]).find(a => a[1] > -1),
            btn = (s, coord) => s.split('').reduce(([i, j], m) => moves[m](i, j), coord);

        return instructions.reduce(
            (c, s) => c + key(btn(s, coords(c[c.length - 1]))), start
        ).slice(1);
    };

    console.log(...keypads.map(k => code(k, input, '5')));
}
