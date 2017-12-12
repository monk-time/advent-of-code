'use strict';

// Note:
// Part 1 is A000045[_26_       + 2] + _19_ * _14_,
// Part 2 is A000045[_26_ + _7_ + 2] + _19_ * _14_
//   where A000045 is the Fibonacci sequence starting from 0,
//   and the underscored numbers are taken from the input in the same order.

{
    // Source optimizations
    const ptnMul = `
        cpy (\\w+) ([a-d])
        inc (?!\\1|\\2)([a-d])
        dec \\2
        jnz \\2 -2
        dec (?!\\1|\\2|\\3)([a-d])
        jnz \\4 -5
    `;
    const ptnAdd = `
        inc ([a-d])
        dec (?!\\1)([a-d])
        jnz \\2 -2
    `;
    const ptnToRegex = ptn => new RegExp(ptn.trim().split('\n').map(s => s.trim()).join('\n'), 'g');
    // mul pattern contains add, so the order is important
    const optimizations = [
        [ptnMul, 'mul $1 $4\nadd $4 $3\ncpy 0 $4\ncpy 0 $2\nnop\nnop'],
        [ptnAdd, 'add $2 $1\ncpy 0 $2\nnop'],
    ];
    const optimize = s => optimizations
        .reduce((acc, [ptn, repl]) => acc.replace(ptnToRegex(ptn), repl), s);

    // Assembunny operations
    const isReg = x => 'abcd'.includes(x);
    const get = (x, reg) => (isReg(x) ? reg[x] : x);
    const set = (r, getValue) => ({ reg, ptr }) => // mutates reg
        ({ reg: Object.assign(reg, { [r]: getValue(reg) }), ptr: ptr + 1 });
    const ops = {
        dec: r => set(r, reg => reg[r] - 1),
        inc: r => set(r, reg => reg[r] + 1),
        cpy: (x, r) => set(r, isReg(x) ? reg => reg[x] : () => x),
        jnz: (x, y) => ({ reg, ptr }) =>
            ({ reg, ptr: ptr + (get(x, reg) !== 0 ? get(y, reg) : 1) }),
        // extended opset
        nop: () => ({ reg, ptr }) => ({ reg, ptr: ptr + 1 }),
        add: (r1, r2) => set(r2, reg => reg[r2] + reg[r1]),
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
    const execute = (program, reg = { ...regZero }, ptr = 0) => {
        while (ptr >= 0 && ptr < program.length) {
            const { op, args } = program[ptr];
            ({ reg, ptr } = ops[op](...args)({ reg, ptr }));
        }

        return reg;
    };

    const input = document.body.textContent.trim();
    const program = parse(optimize(input));
    console.log(execute(program).a, execute(program, { ...regZero, c: 1 }).a);
}
