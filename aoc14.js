'use strict';
function* posTracker({ v, tFly, tRest }) {
    let [pos, remaining, resting] = [0, tFly, false];
    while (true) {
        if (!resting) {
            pos += v;
        }

        if (--remaining === 0) {
            resting = !resting;
            remaining = resting ? tRest : tFly;
        }

        yield pos;
    }
}

function contest(deerArr, time, awardF = state => state) {
    let trackers = deerArr.map(posTracker),
        points = new Array(deerArr.length).fill(0);
    for (let i = 0; i < time; i++) {
        let state = trackers.map(g => g.next().value);
        points = awardF(state, points);
    }

    return Math.max(...points);
}

function awardLeader(state, points) {
    let leader = Math.max(...state);
    return points.map((p, i) => state[i] === leader ? p + 1 : p);
}

let input = document.body.textContent.trim().split('\n'),
    parse = ([v, tFly, tRest]) => ({ v, tFly, tRest }),
    allDeer = input.map(s => s.match(/\d+/g).map(n => +n)).map(parse),
    contestWith = awardF => contest(allDeer, 2503, awardF);

console.log(contestWith(), contestWith(awardLeader));
