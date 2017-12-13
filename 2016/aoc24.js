'use strict';

{
    const parse = arr => { // false == wall
        const stops = [];
        const ducts = arr.map((s, i) => [...s].map((x, j) => {
            if (!'#.'.includes(x)) stops[+x] = [i, j];
            return x === '.' ? true : x === '#' ? false : +x;
        }));
        return { ducts, stops };
    };

    const reachable = (ducts, i, j) => [[i + 1, j], [i - 1, j], [i, j - 1], [i, j + 1]]
        .filter(([y, x]) => ducts[y][x] !== false);
    const shortestDist = (ducts, [i0, j0], [iEnd, jEnd]) => { // bfs
        const dist = { [[i0, j0]]: 0 };
        let [i, j] = [];
        let queue = [[i0, j0]];
        while (queue.length) {
            [[i, j], ...queue] = queue; // dequeue
            if (i === iEnd && j === jEnd) break;
            for (const [iNext, jNext] of reachable(ducts, i, j)) {
                if (dist[[iNext, jNext]] === undefined) { // unvisited
                    dist[[iNext, jNext]] = dist[[i, j]] + 1;
                    queue.push([iNext, jNext]);
                }
            }
        }

        return dist[[i, j]];
    };

    const permute = function* (arr, used = []) {
        if (arr.length === 0)  yield [...used];
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            yield* permute(arr, used);
            arr.splice(i, 0, el);
            used.pop();
        }
    };

    const { ducts, stops } = parse(document.body.textContent.trim().split('\n'));
    const minDists = [...new Array(stops.length)].map(() => [...new Array(stops.length)]);
    for (let i = 0; i < stops.length; i++) {
        for (let j = i; j < stops.length; j++) {
            minDists[i][j] = shortestDist(ducts, stops[i], stops[j]);
            minDists[j][i] = minDists[i][j];
        }
    }

    const routeLen = seq => seq.slice(1).reduce((n, x, i) => n + minDists[seq[i]][x], 0);
    const paths = [...permute(stops.slice(1).map((_, i) => i + 1))];
    const minPath = (returnTo0 = false) => paths
        .map(seq => routeLen([0, ...seq]) + (returnTo0 && minDists[seq[seq.length - 1]][0]))
        .reduce((min, x) => Math.min(min, x));
    console.log(minPath(), minPath(true));
}
