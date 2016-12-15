'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const discs = input.map(s => (([, n, , n0]) => [+n, +n0])(s.match(/\d+/g)));
    const bounces = (discs, time) => discs.some(([n, n0], i) => (n0 + time + i + 1) % n !== 0);
    const minTime = (discs, time = -1) => {
        while (bounces(discs, ++time));
        return time;
    };

    console.log(minTime(discs), minTime([...discs, [11, 0]]));
}
