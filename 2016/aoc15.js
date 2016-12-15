'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const discs = input.map(s => (([, n, , start]) => [+n, +start])(s.match(/\d+/g)));
    const minTime = discs => {
        let [time, bounced] = [-1, true];
        while (bounced) {
            time++;
            bounced = discs.some(([n, start], i) => (start + time + i + 1) % n !== 0);
        }
        return time;
    };

    console.log(minTime(discs), minTime([...discs, [11, 0]]));
}
