// https://adventofcode.com/2017/day/16

'use strict';

{
    const movesMap = {
        s: n => a => [...a.slice(a.length - n), ...a.slice(0, a.length - n)],
        p: (x, y) => a => a.map(z => (z === x ? y : z === y ? x : z)),
        x: (i, j) => a => a.map((z, k) => (k === i ? a[j] : k === j ? a[i] : z)),
    };

    const input = document.body.textContent.trim();
    const parseArg = x => (Number.isNaN(+x) ? x : +x);
    const getMove = ([, m, ...args]) => movesMap[m](...args.map(parseArg));
    const moves = input.split(',')
        .map(s => getMove(s.match(/([sxp])([a-p]|\d+)(?:\/([a-p]|\d+))?/)));
    const dance = a => moves.reduce((acc, m) => m(acc), a);

    const findLoop = (state, f) => {
        let [key, i] = [state.join(''), 0];
        const cache = {};
        while (!(key in cache)) {
            cache[key] = i;
            state = f(state);
            [key, i] = [state.join(''), i + 1];
        }

        return [i, Object.keys(cache).length - cache[key], cache];
    };

    const programs = [...'abcdefghijklmnop'];
    console.log(dance(programs).join(''));

    const [before, loopLen, loop] = findLoop(programs, dance);
    const finalPos = (1000000000 - before) % loopLen;
    console.log(Object.entries(loop).find((a, i) => i === finalPos)[0]);
}
