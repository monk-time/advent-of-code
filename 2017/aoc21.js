'use strict';

{
    // Parsing
    const hash = a => a.reduce((n, bit) => (n << 1) + bit); // eslint-disable-line no-bitwise
    const parseCell = cell => cell.match(/#|\./g).map(ch => '.#'.indexOf(ch));
    const parseRules = lines => lines.map(s => s.split('=>').map(parseCell))
        .reduce((o, [from, to]) => Object.assign(o, { [hash(from)]: to }), {});
    const lines = document.body.textContent.trim().split('\n');
    const splitAt = lines.findIndex(s => s.length > 20);
    const rules = {
        2: parseRules(lines.slice(0, splitAt)),
        3: parseRules(lines.slice(splitAt)),
    };

    // Cells (patterns) are represented by arrays of elements (top to bottom, LTR)
    const cellOps = {
        2: {
            rotate: ([a, b, c, d]) => [c, a, d, b],
            flipH:  ([a, b, c, d]) => [b, a, d, c],
            flipV:  ([a, b, c, d]) => [c, d, a, b],
        },
        3: {
            rotate: ([a, b, c, d, e, f, g, h, i]) => [g, d, a, h, e, b, i, f, c],
            flipH:  ([a, b, c, d, e, f, g, h, i]) => [c, b, a, f, e, d, i, h, g],
            flipV:  ([a, b, c, d, e, f, g, h, i]) => [g, h, i, d, e, f, a, b, c],
        },
    };

    const dot = (f, g) => x => f(g(x));
    const allOps = size => (({ rotate: r, flipH: h, flipV: v }) =>
        [x => x, r, h, v, dot(r, r), dot(dot(r, r), r), dot(r, v), dot(r, h)]
    )(cellOps[size]);

    // const getCellVariants = (cell, size) => allOps(size).map(f => f(cell));

    // Image manipulation
    const cellAt = function* (a, i, j, size) {
        for (let k = 0; k < size ** 2; k++) {
            yield a[i + Math.floor(k / size)][j + (k % size)];
        }
    };

    const applyRules = function* (a) {
        const size = a.length % 2 === 0 ? 2 : 3;
        for (let i = 0; i < a.length; i += size) {
            for (let j = 0; j < a.length; j += size) {
                const cell = [...cellAt(a, i, j, size)];
                let yielded = false;
                for (const op of allOps(size)) {
                    const match = rules[size][hash(op(cell))];
                    if (!match) continue;
                    yield match;
                    yielded = true;
                    break;
                }

                if (!yielded) throw new Error('This should never happen.');
            }
        }
    };

    const stitch = cells => {
        const size = Math.sqrt(cells[0].length);
        const cellsInARow = Math.sqrt(cells.length);
        const width = cellsInARow * size;
        const a = [...new Array(width)].map(() => [...new Array(width)]);
        for (let i = 0; i < a.length; i++) {
            for (let j = 0; j < a.length; j++) {
                const cellInd = cellsInARow * Math.floor(i / size) + Math.floor(j / size);
                const pxlInd = size * (i % size) + j % size;
                a[i][j] = cells[cellInd][pxlInd];
            }
        }

        return a;
    };

    const step = a => stitch([...applyRules(a)]);
    const start = [[0, 1, 0], [0, 0, 1], [1, 1, 1]];
    const nSteps = (n, a0 = start) => [...new Array(n)].reduce(a => step(a), a0);
    const sum = a => a.reduce((n, row) => n + row.reduce((x, y) => x + y), 0);

    const step5 = nSteps(5);
    console.log(sum(step5), sum(nSteps(13, step5))); // 11 sec

    // TODO: try replacng flips with x-y inversions
    // TODO: 3 iterations of a 3x3 image is a 9x9 image
}
