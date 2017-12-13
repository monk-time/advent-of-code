'use strict';

{
    const parse = s => (([from, to]) => [+from, +to])(s.match(/\d+/g));
    const allowed = (blocked, max) => blocked.reduce((acc, [fromX, toX]) => {
        const acc2 = [];
        for (let [from, to] of acc) { // intersect all allowed ranges with a blacklisted range
            // [x][v], [x[xv]v], [xv|v]
            if (fromX <= from && toX <  to) from = Math.max(toX + 1, from);
            // [v][x], [v[xv]x], [v|xv]
            if (fromX >  from && toX >= to) to = Math.min(fromX - 1, to);
            // [x[xv]x], [xv|x], [x|xv]
            if (fromX <= from && toX >= to) continue;
            // [v[xv]v]
            if (fromX >  from && toX <  to) {
                acc2.push([from, fromX - 1], [toX + 1, to]);
                continue;
            }

            acc2.push([from, to]);
        }

        return acc2;
    }, [[0, max]]);
    const ipCount = ranges => ranges.reduce((n, [from, to]) => n + to - from + 1, 0);

    const input = document.body.textContent.trim().split('\n').map(parse);
    const whitelist = allowed(input, 4294967295);
    console.log(whitelist[0][0], ipCount(whitelist));
}
