'use strict';
function* posTracker(deer) {
    let [pos, remaining, resting] = [0, deer.tFly, false];
    while (true) {
        if (!resting) {
            pos += deer.v;
        }

        if (--remaining === 0) {
            resting = !resting;
            remaining = resting ? deer.tRest : deer.tFly;
        }

        yield pos;
    }
}

function contest(deerArr, time, awardF = pos => pos) {
    let trackers = deerArr.map(posTracker),
        points = new Array(deerArr.length).fill(0);
    for (let i = 0; i < time; i++) {
        let pos = trackers.map(g => g.next().value);
        points = awardF(pos, points);
    }

    return Math.max(...points);
}

function awardLeader(pos, points) {
    let leader = Math.max(...pos);
    return points.map((p, i) => pos[i] === leader ? p + 1 : p);
}

let input = document.body.textContent.trim().split('\n'),
    parse = ([v, tFly, tRest]) => ({ v, tFly, tRest }),
    allDeer = input.map(s => s.match(/\d+/g).map(n => +n)).map(parse),
    contestWith = awardF => contest(allDeer, 2503, awardF);

console.log(contestWith(), contestWith(awardLeader));
