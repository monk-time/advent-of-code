'use strict';

{
    const posTracker = function* ({ v, tFly, tRest }) {
        let [pos, remaining, resting] = [0, tFly, false];
        while (true) {
            if (!resting) pos += v;
            if (--remaining === 0) {
                resting = !resting;
                remaining = resting ? tRest : tFly;
            }

            yield pos;
        }
    };

    const contest = (deers, time, awardF = state => state) => {
        const trackers = deers.map(posTracker);
        let points = new Array(deers.length).fill(0);
        for (let t = 0; t < time; t++) {
            const state = trackers.map(tr => tr.next().value);
            points = awardF(state, points);
        }

        return Math.max(...points);
    };

    const awardLeader = (state, points) => {
        const leader = Math.max(...state);
        return points.map((p, i) => (state[i] === leader ? p + 1 : p));
    };

    const input = document.body.textContent.trim().split('\n');
    const parse = ([v, tFly, tRest]) => ({ v, tFly, tRest });
    const deers = input.map(s => s.match(/\d+/g).map(Number)).map(parse);
    const contestWith = awardF => contest(deers, 2503, awardF);

    console.log(contestWith(), contestWith(awardLeader));
}
