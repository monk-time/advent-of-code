// https://adventofcode.com/2016/day/22

'use strict';

{
    const getNode = ([x, y, size, used, avail]) => ({ x, y, size, used, avail });
    const parseNode = s => getNode(s.match(/\d+/g).map(n => +n));
    const values = (key, nodes) => [...new Set(nodes.map(n => n[key]))].sort((a, b) => a - b);
    const [empty, full, avg, goal] = [0, 1, 2, 3];
    const getGrid = nodes => {
        const [l, h] = ['x', 'y'].map(key => values(key, nodes).slice(-1)[0]);
        const grid = [...new Array(h + 1)].map(() => new Array(l + 1));
        const minSize = values('size', nodes)[0];
        for (const n of nodes) {
            grid[n.y][n.x] = n.x === l && n.y === 0 ? goal :
                n.used === 0 ? empty :
                    n.size < minSize * 2 ? avg : full;
        }

        return grid;
    };

    const viablePairs = grid => grid.reduce((sum, row) =>
        sum + row.filter(n => n >= avg).length, 0);
    const minSteps = grid => {
        let posEmpty;
        let posLeftWall;
        for (let y = 0; y < grid.length; y++) {
            for (let x = 0; x < grid[0].length; x++) {
                if (grid[y][x] === empty) {
                    posEmpty = { x, y };
                } else if (!posLeftWall && grid[y][x] === full) {
                    posLeftWall = { x, y };
                }
            }
        }

        const upToTheWall = posEmpty.y - posLeftWall.y - 1;
        const aroundTheWall = posEmpty.x - posLeftWall.x + 1;
        const toTheGoal = posLeftWall.y + 1 + (grid[0].length - posLeftWall.x);
        return upToTheWall + aroundTheWall + toTheGoal + 5 * (grid[0].length - 2);
    };

    const input = document.body.textContent.trim().split('\n').slice(2);
    const grid = getGrid(input.map(parseNode));
    console.log(viablePairs(grid), minSteps(grid));
}
