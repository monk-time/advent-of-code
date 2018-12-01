'use strict';

{
    const apply = f => r => ({ mem, ptr }) => ({ mem: { ...mem, [r]: f(mem[r]) }, ptr: ptr + 1 });
    const jump =  n =>      ({ mem, ptr }) => ({ mem, ptr: ptr + n });
    const jumpIf = f => (r, n) => ({ mem, ptr }) => ({ mem, ptr: ptr + (f(mem[r]) ? n : 1) });

    const cmds = {
        hlf: apply(x => x / 2),
        tpl: apply(x => x * 3),
        inc: apply(x => x + 1),
        jmp: jump,
        jie: jumpIf(x => x % 2 === 0),
        jio: jumpIf(x => x === 1),
    };

    const parse = line => {
        const [, cmd, r, n] = line.match(/([a-z]{3}) ([a-z])?(?:, )?([-+]\d+)?/);
        const args = r ? n ? [r, +n] : [r] : [+n];
        return cmds[cmd](...args);
    };

    const run = (program, state) => {
        while (state.ptr < program.length) {
            state = program[state.ptr](state);
        }

        return state;
    };

    const program = document.body.textContent.trim().split('\n').map(parse);
    const state = a => ({ mem: { a, b: 0 }, ptr: 0 });

    console.log([0, 1].map(n => run(program, state(n)).mem.b));
}
