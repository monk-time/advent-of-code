'use strict';
{
    let reg, program, signal;
    const isReg = x => 'abcd'.includes(x);
    const set = (r, value) => ptr => (reg[r] = value(), ptr + 1);
    const nop = ptr => ptr + 1;
    const ops = {
        inc: r => set(r, () => reg[r] + 1),
        dec: r => set(r, () => reg[r] - 1),
        cpy: (x, r) => isReg(r) ? set(r, isReg(x) ? () => reg[x] : () => x) : nop,
        jnz: (x, y) => isReg(x) ?
            isReg(y) ?
                ptr => reg[x] !== 0 ? ptr + reg[y] : ptr + 1 :
                ptr => reg[x] !== 0 ? ptr + y      : ptr + 1 :
            x !== 0 ? (isReg(y) ? ptr => ptr + reg[y] : ptr => ptr + y) : nop,
        out: x => ptr => (signal.push(reg[x]), ptr + 1)
    };
    const parseLine = s => s.match(/([a-z]{3}) (-?\w+)(?: (-?\w+))?/);
    const parseArg = x => x && (isReg(x) ? x : +x);
    const compile = arr => arr.map(parseLine).map(([, op, ...args]) => {
        if (args[1] === undefined) {
            args = [args[0]];
        }
        const line = { op, args: args.map(parseArg) };
        return line;
    });

    const mulOps = 'cpy,cpy,cpy,inc,dec,jnz,dec,jnz';
    const mulRe = /([a-z]),(?!\1)([a-z]);0,\1;(?!\1|\2)([a-z]),(?!\1|\2|\3)([a-z]);\1;\4;\4,-2;\2;\2,-5/;
    // const logBefore = (ptr, op, x, y) => `Executing ${('@' + ptr).padStart(4)}: ` +
    //     `|${op.padEnd(4)} ${(x + '').padStart(3)} ${((y || '') + '').padStart(3)}|`;
    // const logAfter = (msg, mark = ' ') => console.log(
    //     `${msg}${mark} --> reg: ${[...'abcd'].map(x => (reg[x] + '').padStart(7)).join('')}`);
    let execute = (regA = 0) => {
        signal = [];
        reg = { a: 0, b: 0, c: 0, d: 0 };
        reg.a = regA;
        let [ptr, counter] = [0, 0];
        let [msg, stop] = ['', 30000];
        // console.log(ptr, reg);
        while (ptr >= 0 && ptr < program.length && counter < stop) {
            counter++;
            const { op, args } = program[ptr];
            if (['inc', 'dec'].includes(op) && ptr + 2 < program.length) {
                // ADD optimization
                const [line2, line3] = [program[ptr + 1], program[ptr + 2]];
                const properArgs = line2.args[0] === line3.args[0] && line3.args[1] === -2;
                if (line2.op === 'dec' && line3.op === 'jnz' && properArgs) {
                    // msg = logBefore(ptr, 'add', line2.args[0], args[0]);
                    if (op === 'inc') {
                        reg[args[0]] += reg[line2.args[0]];
                    } else {
                        reg[args[0]] -= reg[line2.args[0]];
                    }
                    reg[line2.args[0]] = 0;
                    ptr += 3;
                    // if (counter < stop) logAfter(msg, '+');
                    continue;
                }
            } else if (ptr + 7 < program.length && op === 'cpy' && program[ptr + 1].op === 'cpy') {
                // MUL optimization
                const fragment = program.slice(ptr, ptr + 8);
                const properOps = () => fragment.map(l => l.op).join(',') === mulOps;
                const properArgs = () => mulRe.test(fragment.map(l => l.args.join(',')).join(';'));
                if (properOps() && properArgs()) {
                    // msg = logBefore(ptr, 'mul', program[ptr + 2].args[0], args[0]);
                    reg[args[0]] *= reg[program[ptr + 2].args[0]];
                    reg[args[1]] = 0;
                    reg[program[ptr + 2].args[1]] = 0;
                    ptr += 8;
                    // if (counter < stop) logAfter(msg, '*');
                    continue;
                }
            }
            // msg = logBefore(ptr, op, ...args);
            ptr = ops[op](...args)(ptr);
            if (op === 'out') {
                if (signal.length >= 2) {
                    if (signal[signal.length - 1] === signal[signal.length - 2]) {
                        return false;
                    }
                }
            }
            // if (counter < stop) logAfter(msg);
        }
        // console.log(`Executed ${counter} instructions`);
        return reg;
    };

    const input = document.body.textContent.trim().split('\n');
    program = compile(input);
    let regA = 0;
    while (!execute(regA)) {
        regA++;
    }
    console.log(regA);
}
