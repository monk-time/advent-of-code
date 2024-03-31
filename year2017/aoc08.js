// https://adventofcode.com/2017/day/8

'use strict';

{
    /* eslint-disable no-eval */
    const parse = s => s.match(/(\w+) ((?:in|de)c) (-?\d+) if (\w+) ([!><=]=?) (-?\d+)/);
    const ops = { inc: '+', dec: '-' };
    const memEval = (r, op, n) => mem => eval(`${mem[r] || 0} ${op} ${n}`);
    const getOp = ([, r, op, n, r2, cmp, n2]) => mem => (memEval(r2, cmp, +n2)(mem) ?
        Object.assign(mem, { [r]: memEval(r, ops[op], +n)(mem) }) : mem);

    const input = document.body.textContent.trim().split('\n');
    const program = input.map(s => getOp(parse(s)));
    const maxReg = mem => Math.max(...Object.values(mem));
    const trackMax = (mem, max) => [mem, Math.max(max, maxReg(mem))];
    const [memEnd, maxEnd] = program.reduce(([mem, max], op) => trackMax(op(mem), max), [{}, 0]);

    console.log(maxReg(memEnd), maxEnd);
}
