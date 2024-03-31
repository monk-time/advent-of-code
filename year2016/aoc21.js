// https://adventofcode.com/2016/day/21

'use strict';

{
    const parseType = s => s.match(/swap (?:position|letter)|rotate(?: left| right)?|reverse|move/)[0];
    const parseArgs = s => s.match(/ (\d+|[a-z])(?=$| )/g).map(m => m.trim());
    const op = {
        'swap position': (x, y) => a => a.map((c, i) => (i === +x ? a[+y] : i === +y ? a[+x] : c)),
        'swap letter':   (x, y) => a => a.map(c => (c === x ? y : c === y ? x : c)),
        'rotate right': x => a => a.map((_, i) => a[(a.length + i - (+x % a.length)) % a.length]),
        'rotate left':  x => op['rotate right'](-+x),
        rotate: x => a => op['rotate right']((i => i + 1 + (i >= 4 ? 1 : 0))(a.indexOf(x)))(a),
        reverse: (x, y) => a =>
            [...a.slice(0, +x), ...a.slice(+x, +y + 1).reverse(), ...a.slice(+y + 1)],
        move: (x, y) => a => {
            const a2 = [...a];
            a2.splice(+y, 0, ...a2.splice(+x, 1));
            return a2;
        },
    };
    const opR = Object.assign({}, op, {
        'rotate left': op['rotate right'],
        'rotate right': op['rotate left'],
        move: (x, y) => op.move(y, x),
        rotate: x => a => {
            let res = a;
            for (let i = 0; i < a.length; i++) {
                res = op['rotate right'](1)(res);
                if (op.rotate(x)(res).join('') === a.join('')) break;
            }

            return res;
        },
    });

    const input = document.body.textContent.trim().split('\n');
    const exec = (ops, list, pass) => list.reduce((a, s) =>
        ops[parseType(s)](...parseArgs(s))(a), [...pass]).join('');
    console.log(exec(op, input, 'abcdefgh'), exec(opR, input.reverse(), 'fbgdceah'));
}
