'use strict';

{
    const op = (value, dir, state) => (tape, i) => {
        tape[i] = value;
        return [state, i + dir];
    };

    const execute = (rules, state, steps, i = 0) => {
        const tape = {};
        while (steps--) [state, i] = rules[`${state}${tape[i] || 0}`](tape, i);
        return Object.values(tape).reduce((a, b) => a + b);
    };

    const input = document.body.textContent.trim().split('\n\n');
    const [, state0, steps] = input[0].match(/state ([A-Z])\.\n.+?(\d+)/);
    const reOp = /[A-Z](?=[.:])|[01]|left|right/;
    const rules = input.slice(1).map(p => p.split('\n').map(s => s.match(reOp)[0]))
        .reduce((acc, [st, , v0, d0, st0, , v1, d1, st1]) => ({
            ...acc,
            [`${st}0`]: op(+v0, d0 === 'left' ? -1 : 1, st0),
            [`${st}1`]: op(+v1, d1 === 'left' ? -1 : 1, st1),
        }), {});

    console.log(execute(rules, state0, +steps));
}
