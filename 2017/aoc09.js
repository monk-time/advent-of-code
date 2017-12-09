'use strict';

{
    /* eslint-disable key-spacing, space-in-parens */
    const transitions = {
        '1!': ({ i      }) => ({ i:   i + 1               }),
        '1>': (          ) => ({ gb:  false               }),
        '1g': ({ gbN    }) => ({ gbN: gbN + 1             }),
        '0<': (          ) => ({ gb:  true                }),
        '0}': ({ lv     }) => ({ lv:  lv - 1              }),
        '0{': ({ lv, sc }) => ({ lv:  lv + 1, sc: sc + lv }),
    };

    const norm = key => (/1[^!>]/.test(key) ? '1g' : key);
    const nextState = tr => o => Object.assign(o, tr && tr(o));
    const getScore = (s, st = { i: -1, gb: false, gbN: 0, lv: 1, sc: 0 }) => {
        while (++st.i < s.length) {
            st = nextState(transitions[norm(+st.gb + s[st.i])])(st);
        }

        return [st.sc, st.gbN];
    };

    const input = document.body.textContent.trim();
    console.log(getScore(input));
}
