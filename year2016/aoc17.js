/* eslint-disable no-eval */
/* global md5 */

'use strict';

{
    const input = document.querySelector('.puzzle-input').textContent;
    const isValidXY = [(_, y) => y > 0, (_, y) => y < 3, x => x > 0, x => x < 3];
    const delta = [[0, -1], [0, 1], [-1, 0], [1, 0]]; // UDLR
    const isDoorOpen = (x, y) => (ch, i) => isValidXY[i](x, y) && 'bcdef'.includes(ch) &&
          { dir: 'UDLR'[i], coords: [x + delta[i][0], y + delta[i][1]] };
    const openDoors = (code, x = 0, y = 0) =>
        [...md5(code).slice(0, 4)].map(isDoorOpen(x, y)).filter(o => o);

    const bfs = function* (passcode) {
        let [maxSteps, path, x, y] = [0, '', 0, 0];
        const dist = { [path]: 0 }; // empty string is a valid key
        let queue = [[path, x, y]];
        while (queue.length) {
            [[path, x, y], ...queue] = queue; // dequeue
            if (x === 3 && y === 3) {
                if (maxSteps === 0) yield path;
                maxSteps = dist[path];
                continue;
            }

            for (const { dir, coords: [x2, y2] } of openDoors(passcode + path, x, y)) {
                const path2 = path + dir;
                if (dist[path2] === undefined) { // unvisited
                    dist[path2] = dist[path] + 1;
                    queue.push([path2, x2, y2]);
                }
            }
        }

        yield maxSteps;
    };

    fetch('//cdn.jsdelivr.net/npm/js-md5@0.7.2/src/md5.min.js')
        .then(r => r.text()).then(eval).then(() => console.log(...bfs(input)));
}
