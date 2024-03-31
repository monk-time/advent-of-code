// https://adventofcode.com/2015/day/13

'use strict';

{
    const maxPerm = (arr, f, max = 0, used = []) => {
        if (arr.length === 0) return Math.max(max, f([...used]));
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            max = maxPerm(arr, f, max, used);
            arr.splice(i, 0, el);
            used.pop();
        }

        return max;
    };

    const input = document.body.textContent.trim().split('\n');
    const parseLine = s => s.match(/^(\w+).+(gain|lose) (\d+).+?(\w+)\.$/);
    const collect = (acc, [, a, f, n, b]) =>
        ({ ...acc, [a]: { ...acc[a], [b]: f === 'gain' ? +n : -+n } });
    const joyMap = input.map(parseLine).reduce(collect, {});
    const joy = (a, b) => (a === 'Me' ? 0 : joyMap[a][b] + joyMap[b][a]);
    const seat = withMe => seq => seq.reduce(
        ({ prev, sum }, next) => ({ prev: next, sum: sum + joy(prev, next) }),
        { prev: withMe ? 'Me' : seq[seq.length - 1], sum: 0 },
    ).sum;
    const maxJoy = bool => maxPerm(Object.keys(joyMap), seat(bool));

    console.log([false, true].map(maxJoy));
}
