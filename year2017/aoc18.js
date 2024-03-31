// https://adventofcode.com/2017/day/18

'use strict';

{
    const isReg = x => /[a-z]|SOUND/.test(x);
    const get = (x, reg) => (isReg(x) ? reg[x] || 0 : x);
    const set = (r, getValue) => ({ reg, ptr }) =>
        ({ reg: { ...reg, [r]: getValue(reg) }, ptr: ptr + 1 });
    const ops = {
        set: (r, x) => set(r, reg => get(x, reg)),
        add: (r, x) => set(r, reg => reg[r] + get(x, reg)),
        mul: (r, x) => set(r, isReg(x) ? reg => reg[r] * reg[x] : reg => reg[r] * x),
        mod: (r, x) => set(r, reg => reg[r] % get(x, reg)),
        jgz: (x, y) => ({ reg, ptr }) =>
            ({ reg, ptr: ptr + (get(x, reg) > 0 ? get(y, reg) : 1) }),
        snd: x => set('SOUND', reg => get(x, reg)),
        nop: () => ({ reg, ptr }) => ({ reg, ptr: ptr + 1 }),
        rcv: r => set(r, reg => reg.SOUND), // only for part 2
    };

    const parseArg = x => x && (isReg(x) ? x : +x);
    const parseLine = s => {
        const [, op, ...args] = s.match(/^([a-z]{3})(?: (-?\w+)(?: (-?\w+))?)?$/);
        return { op, args: args.map(parseArg) };
    };

    const parse = s => s.split('\n').map(parseLine);

    const execute = program => {
        let state = { reg: {}, ptr: 0 };
        while (state.ptr >= 0 && state.ptr < program.length) {
            let { op, args } = program[state.ptr]; // eslint-disable-line prefer-const
            if (op === 'rcv') {
                if (state.reg[args[0]] > 0) break;
                op = 'nop';
            }

            state = ops[op](...args)(state);
        }

        return state.reg.SOUND;
    };

    const execute2 = function* (program, id) {
        let state = { reg: { p: id }, ptr: 0 };
        while (state.ptr >= 0 && state.ptr < program.length) {
            const { op, args } = program[state.ptr];
            if (op === 'rcv') {
                state.reg.SOUND = yield null;
                if (state.reg.SOUND === undefined) break;
            }

            state = ops[op](...args)(state);
            if (op === 'snd') yield state.reg.SOUND;
        }

        return state;
    };

    const runInParallel = program => {
        const [programA, programB] = [0, 1].map(id => execute2(program, id));
        let [queueA, queueB, resA, resB, counter] = [[], [], programA.next(), programB.next(), 0];
        while (!resA.done || !resB.done) {
            if (resA.value !== null) {
                queueB = [resA.value, ...queueB];
                resA = programA.next();
            } else {
                resA = programA.next(queueA.pop());
            }

            if (resB.value !== null) {
                counter++;
                queueA = [resB.value, ...queueA];
                resB = programB.next();
            } else {
                resB = programB.next(queueB.pop());
            }
        }

        return counter;
    };

    const input = document.body.textContent.trim();
    const program = parse(input);
    console.log(execute(program), runInParallel(program));
}
