'use strict';

{
    const input = +document.querySelector('.puzzle-input').textContent;
    const popcount = n => {
        n = n - ((n >>> 1) & 0x55555555);
        n = (n & 0x33333333) + ((n >>> 2) & 0x33333333);
        return ((n + (n >>> 4) & 0xF0F0F0F) * 0x1010101) >>> 24;
    };
    const f = (x, y) => x * x + 3 * x + 2 * x * y + y + y * y + input;
    const isWall = (x, y) => popcount(f(x, y)) % 2 === 1;
    const maze = (w, h, f = isWall, wall = '\u2588', space = ' ') => [...new Array(h)].map(
        (_, y) => [... new Array(w)].map(
            (_, x) => f(x, y) ? wall : space).join('')).join('\n');
    const safeMoves = (x, y) => [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        .filter(([x0, y0]) => x0 >= 0 && y0 >= 0 && !isWall(x0, y0));
    const dist = {};
    const bfs = (xEnd, yEnd, maxDist) => { // breadth-first search
        dist[[1, 1]] = 0;
        let x, y, queue = [[1, 1]], res = [];
        while (!(res[0] && res[1]) && queue.length) {
            [[x, y], ...queue] = queue; // dequeue
            if (x === xEnd && y === yEnd) {
                res[0] = dist[[x, y]];
            }
            if (!res[1] && dist[[x, y]] === maxDist) {
                res[1] = Object.values(dist).length;
            }
            for (let next of safeMoves(x, y)) {
                if (dist[next] === undefined) { // unvisited
                    dist[next] = dist[[x, y]] + 1;
                    queue.push(next);
                }
            }
        }
        return res;
    };

    console.log(...bfs(31, 39, 50));
}
