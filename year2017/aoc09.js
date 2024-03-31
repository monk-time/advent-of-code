// https://adventofcode.com/2017/day/9

'use strict';

{
    /* eslint-disable space-in-parens */
    const transitions = {
        '1!': ({ i            }) => ({ i: i + 1 }),
        '1>': (                ) => ({ inGarbage: false }),
        '1g': ({ garbageCount }) => ({ garbageCount: garbageCount + 1 }),
        '0<': (                ) => ({ inGarbage: true }),
        '0}': ({ depth        }) => ({ depth: depth - 1 }),
        '0{': ({ depth, score }) => ({ depth: depth + 1, score: score + depth }),
    };

    const norm = key => (/1[^!>]/.test(key) ? '1g' : key);
    const nextState = tr => state => Object.assign(state, tr && tr(state));
    const start = { i: -1, inGarbage: false, garbageCount: 0, depth: 1, score: 0 };
    const getScore = (s, st = start) => {
        while (++st.i < s.length) {
            st = nextState(transitions[norm(+st.inGarbage + s[st.i])])(st);
        }

        return [st.score, st.garbageCount];
    };

    const input = document.body.textContent.trim();
    console.log(getScore(input));
}
