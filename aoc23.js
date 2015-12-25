'use strict';
function parse(line) {
    let [, cmd, r, n] = line.match(/([a-z]{3}) ([a-z])?(?:, )?([-+]\d+)?/),
        args = r ? (n ? [r, +n] : [r]) : [+n];
    return { cmd, args };
}

let apply        = (f, r, mem) => Object.assign({}, mem, { [r]: f(mem[r]) }),
    pickAndApply = f =>  r     => ({ mem, ptr }) => ({ mem: apply(f, r, mem), ptr: ptr + 1 }),
    jump         =          n  => ({ mem, ptr }) => ({ mem, ptr: ptr + n }),
    checkAndJump = f => (r, n) => ({ mem, ptr }) => ({ mem, ptr: ptr + (f(mem[r]) ? n : 1) });

let cmds = {
    hlf: pickAndApply(x => x / 2),
    tpl: pickAndApply(x => x * 3),
    inc: pickAndApply(x => x + 1),
    jmp: jump,
    jie: checkAndJump(x => x % 2 === 0),
    jio: checkAndJump(x => x === 1)
};

function execute(program, state) {
    while (state.ptr < program.length) {
        let { cmd, args } = program[state.ptr];
        state = cmds[cmd](...args)(state);
    }

    return state;
}

let input = document.body.textContent.trim(),
    program = input.split('\n').map(parse),
    state = a => ({ mem: { a, b: 0 }, ptr: 0 });

console.log([0, 1].map(n => execute(program, state(n)).mem.b));
