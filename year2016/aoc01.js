// https://adventofcode.com/2016/day/1

'use strict';

{
    const parseDir = s => ({
        turn: s[0] === 'L' ? -1 : 1,
        blocks: Number(s.slice(1)),
    });
    const dist = ({ x, y }) => Math.abs(x) + Math.abs(y);
    const travel = dirs => dirs.reduce(moveMem, posStart);

    const posStart = { face: 0, x: 0, y: 0 };
    const posRepr = ({ x, y }) => `${x},${y}`;
    const visited = { [posRepr(posStart)]: true };
    let visitedTwice = null;
    const moveMem = (pos, dir) => { // mutates state
        const pos2 = move(pos, dir);
        if (visitedTwice === null) {
            for (const posBtw of visitLine(pos, pos2)) {
                const key = posRepr(posBtw);
                if (!visited[key]) {
                    visited[key] = true;
                } else {
                    visitedTwice = posBtw;
                    break;
                }
            }
        }

        return pos2;
    };

    const move = ({ face, x, y }, { turn, blocks }) => {
        const face2 = (face + turn + 4) % 4;
        const delta = (face2 > 1 ? -1 : 1) * blocks;
        const [x2, y2] = face % 2 === 0 ? [x + delta, y] : [x, y + delta];
        return { face: face2, x: x2, y: y2 };
    };

    const visitLine = ({ x, y }, { x: x2, y: y2 }) => {
        const [from, to, line, axisLine, axisMov] = x === x2 ?
            [y, y2, x, 'x', 'y'] : [x, x2, y, 'y', 'x'];
        const d = from > to ? -1 : 1;
        return [...new Array(Math.abs(to - from)).keys()].map(step =>
            ({ [axisLine]: line, [axisMov]: from + (step + 1) * d }));
    };

    const input = document.body.textContent;
    const seq = input.split(', ').map(parseDir);
    console.log(dist(travel(seq)), dist(visitedTwice));
}
