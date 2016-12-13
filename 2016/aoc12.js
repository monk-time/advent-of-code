'use strict';
// note: Part 1 is A000045[_26_ + 2] + _19_ * _14_,
//       Part 2 is A000045[_26_ + _7_ + 2] + _19_ * _14_
//         where A000045 is the Fibonacci seq starting from 0,
//         and the underscored numbers are taken from the input in the same order.

{
    let reg;
    const set = (r, value) => ptr => (reg[r] = value(), ptr + 1);
    const ops = {
        inc:  r        => set(r, () => reg[r] + 1),
        dec:  r        => set(r, () => reg[r] - 1),
        cpy:  (src, r) => set(r, () => reg[src]),
        cpyN: (num, r) => set(r, () => num),
        jnz:  (src, d) => ptr => reg[src] !== 0 ? ptr + d : ptr + 1,
        jnzN: (num, d) => num !== 0 ? (ptr => ptr + d) : ops.nop(),
        nop:  () => ptr => ptr + 1,
        add:  (src, r) => set(r, () => reg[r] + reg[src]),
    };
    const isReg = x => Number.isNaN(+x);
    const arg = x => isReg(x) ? 'abcd'.indexOf(x) : +x;
    const parse = s => s.match(/([a-z]{3}) (\w+)(?: (-?\w+))?/);
    const compile = arr => arr.map(parse).map(([, op, l, r], i, lines) => {
        op += isReg(l) ? '' : 'N';
        if (i + 2 < arr.length) { // optimization
            const [[, op2, l2], [, op3, l3, r3]] = [lines[i + 1], lines[i + 2]];
            if (op === 'inc' && op2 === 'dec' && op3 === 'jnz' && l2 === l3 && r3 === '-2') {
                [op, l, r] = ['add', l2, l];
                lines[i + 1] = [, 'cpy', '0', l2];
                lines[i + 2][1] = 'nop';
            }
        }
        // const f = ops[op](arg(l), arg(r));
        // f.code = `${op.padEnd(4)} ${(op !== 'nop' ? l : '').padStart(2)} ${(op !== 'nop' ? (r || '') : '').padStart(2)}`;
        // return f;
        return ops[op](arg(l), arg(r));
    });
    let execute = (program, newReg = [0, 0, 0, 0]) => {
        reg = newReg;
        let ptr = 0;
        // let [counter, msg] = [0, ''];
        // console.log(ptr, reg);
        while (ptr >= 0 && ptr < program.length) {
            // counter++;
            // if (counter < 400) msg = `Executing |${program[ptr].code.padEnd(9)}| `;
            ptr = program[ptr](ptr);
            // if (counter < 400) console.log(msg   , (ptr + '').padStart(3), reg);
        }
        // console.log(`Executed ${counter} instructions`);
        return reg;
    };

    const input = document.body.textContent.trim().split('\n');
    const program = compile(input);
    // const timed = f => (...args) => {
    //     console.time('main');
    //     const res = f(...args);
    //     console.timeEnd('main');
    //     return res;
    // };
    // execute = timed(execute);
    console.log(execute(program)[0], execute(program, [0, 0, 1, 0])[0]);
}
