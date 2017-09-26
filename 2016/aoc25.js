'use strict';

{
    // Source optimizations
    const ptnAdd = `
        inc ([a-d])
        dec (?!\\1)([a-d])
        jnz \\2 -2
    `; // TODO: the first might commands can be reversed
    const ptnSub = ptnAdd.replace('inc', 'dec');
    const ptnMul = `
        cpy (\\w+) ([a-d])
        inc (?!\\1|\\2)([a-d])
        dec \\2
        jnz \\2 -2
        dec (?!\\1|\\2|\\3)([a-d])
        jnz \\4 -5
    `;
    const ptnToRegex = ptn => new RegExp(ptn.trim().split('\n').map(s => s.trim()).join('\n'), 'g');
    // mul pattern contains add, so the order is important
    const optimizations = [
        [ptnToRegex(ptnMul), 'mul $1 $4\nadd $4 $3\ncpy 0 $4\ncpy 0 $2\nnop\nnop'],
        [ptnToRegex(ptnAdd), 'add $2 $1\ncpy 0 $2\nnop'],
        [ptnToRegex(ptnSub), 'sub $2 $1\ncpy 0 $2\nnop'],
    ];
    const optimize = s => optimizations
        .reduce((acc, [re, repl]) => acc.replace(re, repl), s);

    // Assembunny operations
    const isReg = x => 'abcd'.includes(x);
    const get = (x, reg) => (isReg(x) ? reg[x] : x);
    const set = (r, getValue) => ({ reg, out, ptr }) => ({
        reg: { ...reg, [r]: getValue(reg) },
        out,
        ptr: ptr + 1,
    });
    const ops = {
        dec: r => set(r, reg => reg[r] - 1),
        inc: r => set(r, reg => reg[r] + 1),
        cpy: (x, r) => set(r, isReg(x) ? reg => reg[x] : () => x),
        jnz: (x, y) => ({ reg, out, ptr }) => ({
            reg,
            out,
            ptr: ptr + (get(x, reg) !== 0 ? get(y, reg) : 1),
        }),
        out: x => ({ reg, out, ptr }) => ({ reg, out: [...out, get(x, reg)], ptr: ptr + 1 }),
        // extended opset
        nop: () => ({ reg, out, ptr }) => ({ reg, out, ptr: ptr + 1 }),
        add: (r1, r2) => set(r2, reg => reg[r2] + reg[r1]),
        sub: (r1, r2) => set(r2, reg => reg[r2] - reg[r1]),
        mul: (x, r) => set(r, isReg(x) ? reg => reg[r] * reg[x] : reg => reg[r] * x),
    };

    // Source parsing
    const parseArg = x => x && (isReg(x) ? x : +x);
    const parseLine = s => {
        const [, op, ...args] = s.match(/^([a-z]{3})(?: (-?\w+)(?: (-?\w+))?)?$/);
        return { op, args: args.map(parseArg) };
    };

    const parse = s => s.split('\n').map(parseLine);

    // Execution
    const regZero = { a: 0, b: 0, c: 0, d: 0 };
    const execute = (program, reg = regZero) => {
        let state = { reg, out: [], ptr: 0 };
        let counter = 0;
        const stop = 30000;
        while (state.ptr >= 0 && state.ptr < program.length && counter++ < stop) {
            const { op, args } = program[state.ptr];
            state = ops[op](...args)(state);
            if (op === 'out' && state.out.length >= 2 &&
                state.out[state.out.length - 1] === state.out[state.out.length - 2]) {
                return null;
            }
        }

        return state;
    };

    const input = document.body.textContent.trim();
    const program = parse(optimize(input));

    let state;
    let regA = 0;
    do {
        regA++; // "the lowest positive" means we need to start from 1
        state = execute(program, { ...regZero, a: regA });
    } while (state === null);

    console.log(regA);
}
