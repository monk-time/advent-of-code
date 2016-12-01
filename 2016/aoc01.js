'use strict';

{
    const parseDir = s => ({
        turn: s[0] === 'L' ? -1 : 1,
        blocks: parseInt(s.slice(1), 10)
    });
    const posStart = { face: 0, x: 0, y: 0 },
        distFromStart = ({ x, y }) => Math.abs(x) + Math.abs(y),
        posRepr = pos => `${pos.x},${pos.y}`;
    const move = ({ face, x, y }, dir) => {
        const face2 = (face + dir.turn + 4) % 4,
            blocksRel = (face2 > 1 ? -1 : 1) * dir.blocks,
            [x2, y2] = face % 2 === 0 ?
                [x + blocksRel, y] : [x, y + blocksRel];
        return { face: face2, x: x2, y: y2 };
    };

    const multidirFor = function* (from, to) {
        const d = from > to ? -1 : 1;
        let i = from;
        while (i !== to) {
            yield i += d;
        }
    };
    const visitLine = function* ({ x: x1, y: y1 }, { x: x2, y: y2 }) {
        const [from, to, line, axisLine, axisMov] = x1 === x2 ?
            [y1, y2, x1, 'x', 'y'] : [x1, x2, y1, 'y', 'x'];
        for (let i of multidirFor(from, to)) {
            yield { [axisLine]: line, [axisMov]: i };
        }
    };

    let visited = [posRepr(posStart)],
        visitedTwice = null;
    const moveMem = (pos, dir) => { // mutates state
        let pos2 = move(pos, dir);
        if (visitedTwice === null) {
            for (let posBtw of visitLine(pos, pos2)) {
                if (!visited.includes(posRepr(posBtw))) {
                    visited.push(posRepr(posBtw));
                } else {
                    visitedTwice = posBtw;
                    break;
                }
            }
        }

        return pos2;
    };
    const travel = dirs => dirs.reduce(moveMem, posStart);

    let input = document.body.textContent,
        seq = input.split(', ').map(parseDir);

    console.log(distFromStart(travel(seq)), distFromStart(visitedTwice));
}
