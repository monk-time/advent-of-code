'use strict';
// basic perm. generator with abstracted out storage function from day 09
function permute(input, pusher = (acc, arr) => acc.push(arr.slice()), acc = []) {
    let used = [];
    function genPerm() {
        if (input.length === 0) {
            pusher(acc, used);
        }

        for (let i = 0; i < input.length; i++) {
            let [el] = input.splice(i, 1);
            used.push(el);
            genPerm();
            input.splice(i, 0, el);
            used.pop();
        }
    }

    genPerm();
    return acc;
}

function collect(acc, [, a, f, n, b]) {
    acc[a] = acc[a] || {};
    acc[a][b] = f === 'lose' ? -+n : +n;
    return acc;
}

function seat(joy, seq, loop = true) {
    let [prev, ...rest] = seq;
    if (loop) {
        rest.push(prev);
    }

    return rest.reduce(({ prev, sum }, next) =>
        ({ prev: next, sum: sum + joy[prev][next] + joy[next][prev] }),
    { prev, sum: 0 }).sum;
}

let input = document.body.textContent.trim().split('\n'),
    parseLine = line => line.match(/^(\w+) .+ (gain|lose) (\d+) .+ (\w+)\.$/),
    joy = input.map(parseLine).reduce(collect, {}),
    seatWithMe = bool => seq => seat(joy, seq, !bool),
    updateMax = f => (acc, arngmt) => acc.max = Math.max(acc.max, f(arngmt)),
    getMax = f => permute(Object.keys(joy), updateMax(f), { max: 0 }).max;

console.log(getMax(seatWithMe(false)), getMax(seatWithMe(true)));
