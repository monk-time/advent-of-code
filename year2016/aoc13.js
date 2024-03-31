// https://adventofcode.com/2016/day/13

/* eslint-disable no-bitwise */

'use strict';

{
    const popcount = n => {
        n -= (n >>> 1) & 0x55555555;
        n = (n & 0x33333333) + ((n >>> 2) & 0x33333333);
        return ((n + (n >>> 4) & 0xF0F0F0F) * 0x1010101) >>> 24;
    };

    const input = +document.querySelector('.puzzle-input').textContent;
    const f = (x, y) => x * x + 3 * x + 2 * x * y + y + y * y + input;
    const isWall = (x, y) => popcount(f(x, y)) % 2 === 1;
    const safeMoves = (x, y) => [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        .filter(([x0, y0]) => x0 >= 0 && y0 >= 0 && !isWall(x0, y0));
    const bfs = (xEnd, yEnd, maxDist) => { // breadth-first search
        let coords = [1, 1];
        let queue = [coords];
        const dist = { [coords]: 0 };
        const res = [];
        while (!(res[0] && res[1]) && queue.length) {
            [coords, ...queue] = queue; // dequeue
            if (coords[0] === xEnd && coords[1] === yEnd) {
                res[0] = dist[coords];
            }

            if (!res[1] && dist[coords] === maxDist) {
                res[1] = Object.values(dist).length;
            }

            for (const next of safeMoves(...coords)) {
                if (dist[next] === undefined) { // unvisited
                    dist[next] = dist[coords] + 1;
                    queue.push(next);
                }
            }
        }

        return res;
    };

    console.log(...bfs(31, 39, 50));
    // const maze = (w, h, g = isWall, wall = '\u2588', space = ' ') => [...new Array(h)]
    //     .map((_, y) => [...new Array(w)]
    //         .map((__, x) => (g(x, y) ? wall : space)).join('')).join('\n');
}
